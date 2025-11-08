from flask import Flask, render_template, request, jsonify
import os
import requests
import json
from pathlib import Path
from websockets.sync.client import connect

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

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"  # Lightweight 1B parameter model

def transcribe_with_soniox(audio_path: str) -> str:
    """
    Transcribe audio file using Soniox API.
    Returns the transcript text.
    """
    if not SONIOX_API_KEY:
        raise RuntimeError("SONIOX_API_KEY is not set. Please set it as an environment variable.")

    # Soniox configuration
    config = {
        "api_key": SONIOX_API_KEY,
        "model": "stt-rt-v3",
        "audio_format": "auto",  # Let Soniox detect the format automatically
    }

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

@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']

        # Save the audio file temporarily
        audio_path = os.path.join(UPLOAD_FOLDER, 'recording.wav')
        audio_file.save(audio_path)

        # Transcribe using Soniox
        print("Transcribing audio with Soniox...")
        transcript = transcribe_with_soniox(audio_path)
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
    print("Speech-to-Text AI Assistant (Soniox + Ollama)")
    print("=" * 50)
    if SONIOX_API_KEY:
        print("Soniox API: Configured")
    else:
        print("WARNING: Soniox API key not set!")
        print("Set with: export SONIOX_API_KEY=<your_api_key>")
    print("Starting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
