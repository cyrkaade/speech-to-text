from flask import Flask, render_template, request, jsonify
import os
import whisper
import requests
from pathlib import Path

app = Flask(__name__, template_folder='.')

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper model (using tiny model for lightweight performance)
print("Loading Whisper model...")
whisper_model = whisper.load_model("tiny")
print("Whisper model loaded!")

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"  # Lightweight 1B parameter model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']

        # Save the audio file temporarily
        audio_path = os.path.join(UPLOAD_FOLDER, 'recording.wav')
        audio_file.save(audio_path)

        # Transcribe using Whisper
        print("Transcribing audio...")
        result = whisper_model.transcribe(audio_path)
        transcript = result["text"]
        print(f"Transcript: {transcript}")

        # Clean up the audio file
        os.remove(audio_path)

        return jsonify({
            'transcript': transcript
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

        print(f"Getting AI response for: {user_text}")

        # Call Ollama API
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": user_text,
                "stream": False
            },
            timeout=60
        )

        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code}")

        ai_response = response.json()['response']
        print(f"AI Response: {ai_response}")

        return jsonify({
            'response': ai_response
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Could not connect to Ollama. Make sure Ollama is running (ollama serve) and the model is installed.'
        }), 500
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request to Ollama timed out. The model might be too slow or not responding.'
        }), 500
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Speech-to-Text AI Assistant")
    print("=" * 50)
    print("Starting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
