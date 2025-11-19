from flask import Flask, render_template, request, jsonify
import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from websockets.sync.client import connect
from openai import OpenAI
from medicaments_vocabulary import get_compact_speech_context

app = Flask(__name__, template_folder='.')

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Soniox API configuration
SONIOX_API_KEY = os.environ.get("SONIOX_API_KEY")
SONIOX_WEBSOCKET_URL = "wss://stt-rt.soniox.com/transcribe-websocket"

if not SONIOX_API_KEY:
    print("WARNING: SONIOX_API_KEY environment variable not set!")
    print("Please set it with: export SONIOX_API_KEY=<your_api_key>")

# OpenAI configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY environment variable not set!")
    print("Please set it with: export OPENAI_API_KEY=<your_api_key>")

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Database configuration
DATABASE = 'questionnaire.db'

def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            weight TEXT,
            heart_rate TEXT,
            edema TEXT,
            smoking_status TEXT,
            cigarette_count TEXT,
            daily_routine_medications TEXT,
            ai_score INTEGER,
            ai_feedback TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully")

# Initialize database on startup
init_db()

def transcribe_with_soniox(audio_path: str, language: str = "ru") -> str:
    """
    Transcribe audio file using Soniox API with medicament recognition.

    Args:
        audio_path: Path to the audio file
        language: Language code ("ru" for Russian, "kk" for Kazakh, "multi" for auto-detect)

    Returns:
        The transcript text.
    """
    if not SONIOX_API_KEY:
        raise RuntimeError("SONIOX_API_KEY is not set. Please set it as an environment variable.")

    # Get medicament vocabulary for speech context
    speech_context = get_compact_speech_context(boost_medicaments=20, boost_medical_terms=15)

    # Soniox configuration
    config = {
        "api_key": SONIOX_API_KEY,
        "model": "stt-rt-v3",
        "audio_format": "auto",  # Let Soniox detect the format automatically
        "speech_context": speech_context,  # Add custom vocabulary for medicaments
    }

    # Add language if specified
    if language and language != "multi":
        config["language"] = language

    print("Connecting to Soniox...")
    with connect(SONIOX_WEBSOCKET_URL) as ws:
        # Send configuration
        ws.send(json.dumps(config))

        # Stream audio file
        print("Streaming audio to Soniox...")
        with open(audio_path, "rb") as fh:
            while True:
                data = fh.read(3840)
                if len(data) == 0:
                    break
                ws.send(data)

        # Send end-of-audio signal
        ws.send("")

        # Collect transcript from responses
        transcript_parts = []

        print("Receiving transcription...")
        while True:
            message = ws.recv()
            response = json.loads(message)

            # Check for errors
            if response.get("error_code") is not None:
                error_msg = f"{response['error_code']}: {response.get('error_message', 'Unknown error')}"
                raise RuntimeError(f"Soniox API error: {error_msg}")

            # Extract final tokens (only final tokens are stored)
            for token in response.get("tokens", []):
                if token.get("is_final") and token.get("text"):
                    transcript_parts.append(token["text"])

            # Check if finished
            if response.get("finished"):
                break

        transcript = "".join(transcript_parts)
        print(f"Transcription complete: {transcript}")
        return transcript

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']

        # Get language parameter (default to auto-detect for questionnaire compatibility)
        language = request.form.get('language', 'multi')

        # Save the audio file temporarily
        audio_path = os.path.join(UPLOAD_FOLDER, 'recording.wav')
        audio_file.save(audio_path)

        # Transcribe using Soniox with medicament recognition
        print(f"Transcribing audio with Soniox (language: {language})...")
        transcript = transcribe_with_soniox(audio_path, language=language)
        print(f"Transcript: {transcript}")

        # Clean up the audio file
        os.remove(audio_path)

        return jsonify({
            'transcript': transcript,
            'language': language
        })

    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-ai-response', methods=['POST'])
def get_ai_response():
    try:
        data = request.json
        user_text = data.get('text', '')

        if not user_text:
            return jsonify({'error': 'No text provided'}), 400

        if not openai_client:
            return jsonify({
                'error': 'OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.'
            }), 500

        print(f"Getting AI response for: {user_text}")

        # Call OpenAI GPT-4 API
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Respond naturally and conversationally."},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=500
        )

        ai_response = response.choices[0].message.content
        print(f"AI Response: {ai_response}")

        return jsonify({
            'response': ai_response
        })

    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return jsonify({'error': str(e)}), 500

def get_ai_feedback(answers):
    """
    Send questionnaire answers to OpenAI and get health feedback with score
    """
    try:
        prompt = f"""You are a medical health advisor. Based on the following patient questionnaire responses in Russian, provide:
1. A health risk score from 0-100 (0 = excellent health, 100 = high risk)
2. Detailed feedback and recommendations in Russian

Patient Responses:
- Вес (Weight): {answers.get('1', 'Не указано')}
- ЧСС (Heart Rate): {answers.get('2', 'Не указано')}
- Наличие отеков (Edema): {answers.get('3', 'Не указано')}
- Статус курения (Smoking): {answers.get('4', 'Не указано')}
- Кол-во сигарет (Cigarettes per day): {answers.get('5', 'Не указано')}
- Как прошел день и какие таблетки пили (Daily routine and medications): {answers.get('6', 'Не указано')}

Provide your response in the following JSON format:
{{
    "score": <number 0-100>,
    "feedback": "<detailed feedback in Russian>"
}}"""

        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a medical health advisor providing health risk assessments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        result_text = response.choices[0].message.content

        # Try to parse JSON response
        try:
            result = json.loads(result_text)
            return result['score'], result['feedback']
        except json.JSONDecodeError:
            # If not JSON, extract score and use full text as feedback
            import re
            score_match = re.search(r'"score"\s*:\s*(\d+)', result_text)
            score = int(score_match.group(1)) if score_match else 50
            return score, result_text

    except Exception as e:
        print(f"Error getting AI feedback: {str(e)}")
        return 50, f"Ошибка при получении обратной связи: {str(e)}"

@app.route('/submit-questionnaire', methods=['POST'])
def submit_questionnaire():
    try:
        data = request.json
        answers = data.get('answers', {})

        if not answers:
            return jsonify({'error': 'No answers provided'}), 400

        print("=" * 50)
        print("Questionnaire Submitted:")
        print("=" * 50)

        # Get AI feedback
        print("Getting AI feedback from OpenAI...")
        ai_score, ai_feedback = get_ai_feedback(answers)
        print(f"AI Score: {ai_score}")
        print(f"AI Feedback: {ai_feedback[:100]}...")

        # Save to database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO responses (weight, heart_rate, edema, smoking_status, cigarette_count, daily_routine_medications, ai_score, ai_feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            answers.get('1', ''),
            answers.get('2', ''),
            answers.get('3', ''),
            answers.get('4', ''),
            answers.get('5', ''),
            answers.get('6', ''),
            ai_score,
            ai_feedback
        ))

        response_id = cursor.lastrowid
        conn.commit()
        conn.close()

        print(f"Saved to database with ID: {response_id}")
        print("=" * 50)

        return jsonify({
            'success': True,
            'message': 'Questionnaire submitted successfully',
            'response_id': response_id,
            'score': ai_score
        })

    except Exception as e:
        print(f"Error submitting questionnaire: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-feedback/<int:response_id>', methods=['GET'])
def get_feedback(response_id):
    """Retrieve AI feedback for a specific response"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT ai_score, ai_feedback, weight, heart_rate, edema, smoking_status, cigarette_count, daily_routine_medications, submission_time
            FROM responses
            WHERE id = ?
        ''', (response_id,))

        result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({'error': 'Response not found'}), 404

        return jsonify({
            'success': True,
            'score': result[0],
            'feedback': result[1],
            'answers': {
                'weight': result[2],
                'heart_rate': result[3],
                'edema': result[4],
                'smoking_status': result[5],
                'cigarette_count': result[6],
                'daily_routine_medications': result[7]
            },
            'submission_time': result[8]
        })

    except Exception as e:
        print(f"Error retrieving feedback: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Speech-to-Text AI Assistant (Soniox + GPT-4)")
    print("=" * 50)
    if SONIOX_API_KEY:
        print("Soniox API: Configured")
    else:
        print("WARNING: Soniox API key not set!")
        print("Set with: export SONIOX_API_KEY=<your_api_key>")
    if OPENAI_API_KEY:
        print("OpenAI API: Configured")
    else:
        print("WARNING: OpenAI API key not set!")
        print("Set with: export OPENAI_API_KEY=<your_api_key>")
    print("Starting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
