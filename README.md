# Speech-to-Text AI Assistant

A lightweight local speech-to-text application that records your voice, converts it to text using OpenAI's Whisper model, and gets AI responses using Ollama.

## Features

- Record audio directly from your browser
- Local speech-to-text using Whisper (tiny model - ~39MB)
- Local LLM responses using Ollama (llama3.2:1b - ~1.3GB)
- Clean, modern web interface
- No cloud services required - everything runs locally

## Prerequisites

1. **Python 3.8+**
2. **Ollama** - For local LLM inference

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Note: The first time you run the app, Whisper will download the tiny model (~39MB).

### 2. Install and Setup Ollama

#### Windows:
1. Download Ollama from: https://ollama.ai/download
2. Install and run Ollama
3. Open a command prompt and run:
```bash
ollama pull llama3.2:1b
```

#### Mac/Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:1b
```

### 3. Start Ollama Server

Make sure Ollama is running:
```bash
ollama serve
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open Your Browser

Navigate to: http://localhost:5000

## Usage

1. Click the "Start Recording" button
2. Speak into your microphone
3. Click "Stop Recording" when done
4. Wait for the transcript to appear
5. The AI will automatically generate a response to your speech

## Models Used

- **Speech-to-Text**: Whisper Tiny (~39MB)
  - Fast and lightweight
  - Good accuracy for most use cases
  - Runs on CPU

- **LLM**: Llama 3.2 1B (~1.3GB)
  - Lightweight but capable
  - Fast inference on CPU
  - Good for general conversations

## Upgrading Models (Optional)

### For better transcription accuracy:
Replace `tiny` with `base`, `small`, or `medium` in [app.py:17](app.py#L17):
```python
whisper_model = whisper.load_model("base")  # ~74MB
# whisper_model = whisper.load_model("small")  # ~244MB
# whisper_model = whisper.load_model("medium")  # ~769MB
```

### For better AI responses:
Replace the model in [app.py:21](app.py#L21):
```python
OLLAMA_MODEL = "llama3.2:3b"  # Better responses, ~3GB
```

Then pull the new model:
```bash
ollama pull llama3.2:3b
```

## Troubleshooting

### "Could not connect to Ollama"
- Make sure Ollama is installed and running: `ollama serve`
- Check if the model is installed: `ollama list`

### "Could not access microphone"
- Grant microphone permissions in your browser
- Check browser console for detailed errors

### Slow transcription
- The tiny model should be fast on most CPUs
- Consider using GPU acceleration if available (PyTorch with CUDA)

### Port already in use
Change the port in [app.py:99](app.py#L99):
```python
app.run(debug=True, port=5001)
```

## License

MIT
