# Speech-to-Text AI Assistant

A speech-to-text application that records your voice, converts it to text using Soniox API, and gets AI responses using Ollama.

## Features

- Record audio directly from your browser
- Cloud-based speech-to-text using Soniox API (high accuracy, real-time)
- Local LLM responses using Ollama (llama3.2:1b - ~1.3GB)
- Clean, modern web interface
- Supports multiple languages and speaker diarization

## Prerequisites

1. **Python 3.8+**
2. **Soniox API Key** - Get yours at https://console.soniox.com
3. **Ollama** - For local LLM inference

## Setup Instructions

### 1. Get Soniox API Key

1. Sign up at https://console.soniox.com
2. Get your API key from the console
3. Set it as an environment variable:

**Windows (Command Prompt):**
```cmd
set SONIOX_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:SONIOX_API_KEY="your_api_key_here"
```

**Mac/Linux:**
```bash
export SONIOX_API_KEY=your_api_key_here
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install and Setup Ollama

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

### 4. Start Ollama Server

Make sure Ollama is running:
```bash
ollama serve
```

### 5. Run the Application

```bash
python app.py
```

### 6. Open Your Browser

Navigate to: http://localhost:5000

## Usage

1. Click the "Start Recording" button
2. Speak into your microphone
3. Click "Stop Recording" when done
4. Wait for the transcript to appear
5. The AI will automatically generate a response to your speech

## Models Used

- **Speech-to-Text**: Soniox API (stt-rt-v3)
  - High accuracy cloud-based transcription
  - Real-time processing
  - Supports multiple languages
  - Speaker diarization and language identification

- **LLM**: Llama 3.2 1B (~1.3GB)
  - Lightweight but capable
  - Fast inference on CPU
  - Good for general conversations

## Configuration (Optional)

### Customize Soniox settings:
Edit the `transcribe_with_soniox` function in app.py:app.py:26 to customize:
- Language hints
- Enable/disable speaker diarization
- Enable/disable language identification
- Set context for domain-specific vocabulary
- Enable translation

### For better AI responses:
Replace the model in app.py:23:
```python
OLLAMA_MODEL = "llama3.2:3b"  # Better responses, ~3GB
```

Then pull the new model:
```bash
ollama pull llama3.2:3b
```

## Troubleshooting

### "SONIOX_API_KEY is not set"
- Make sure you've set the environment variable
- On Windows, restart your terminal after setting the variable
- Check the variable is set: `echo %SONIOX_API_KEY%` (Windows) or `echo $SONIOX_API_KEY` (Mac/Linux)

### "Could not connect to Ollama"
- Make sure Ollama is installed and running: `ollama serve`
- Check if the model is installed: `ollama list`

### "Could not access microphone"
- Grant microphone permissions in your browser
- Check browser console for detailed errors

### Soniox API errors
- Verify your API key is correct
- Check your Soniox account has available credits
- Review error messages in the console for details

### Port already in use
Change the port in app.py:172:
```python
app.run(debug=True, port=5001)
```

## License

MIT
