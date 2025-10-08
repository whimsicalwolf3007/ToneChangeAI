# 🎭 ToneShift AI - Emotion-Aware Real-Time Chat Rewriter

Transform your digital communication with AI-powered emotion analysis and tone rewriting. Make your messages sound exactly how you want them to be perceived.

## ✨ Features

- **Real-time Emotion Analysis**: Detect emotions like happy, sad, angry, sarcastic, and more with confidence scores
- **Intelligent Tone Rewriting**: Transform text into 10+ tone styles (polite, professional, friendly, casual, etc.)
- **WebSocket Support**: Real-time communication for instant feedback and live updates
- **Modern Web Interface**: Beautiful, responsive UI that works on all devices
- **Rule-based Rewriting**: Fast, reliable text transformation using advanced pattern matching
- **Alternative Suggestions**: Get multiple rewrite options for each text
- **Error Handling**: Robust error handling with graceful fallbacks
- **Easy Setup**: One-command installation and startup with `uv`

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd toneshiftai2
   ```

2. **Install dependencies with uv:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env file if needed
   ```

4. **Run the application:**
   ```bash
   uv run python run.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5173`

### Alternative Setup (One Command)

```bash
# Clone, install, and run in one go
git clone <repository-url> && cd toneshiftai2 && uv sync && uv run python run.py
```

## 🎯 Usage

### Web Interface

1. **Enter your message** in the text area
2. **Choose a target tone** from the dropdown
3. **Click "Analyze Emotion"** to see emotion analysis
4. **Click "Rewrite Text"** to transform your message
5. **View suggestions** for alternative phrasings

### API Endpoints

#### Analyze Emotion
```bash
curl -X POST "http://localhost:5173/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!"}' | jq
```

**Response:**
```json
{
  "text": "This is amazing!",
  "emotion_analysis": {
    "emotion": "happy",
    "confidence": 0.5096,
    "all_emotions": {
      "happy": 0.5096,
      "surprised": 0.3812,
      "neutral": 0.0690,
      "angry": 0.0135,
      "sad": 0.0084,
      "fearful": 0.0099,
      "disgusted": 0.0083,
      "sarcasm": 0.0,
      "excited": 0.0,
      "frustrated": 0.0
    }
  },
  "suggestions": [
    "Maintain the positive energy",
    "Share the enthusiasm appropriately"
  ]
}
```

#### Rewrite Text
```bash
curl -X POST "http://localhost:5173/rewrite" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "You need to fix this now!",
    "target_tone": "polite",
    "preserve_meaning": true
  }' | jq
```

**Response:**
```json
{
  "original_text": "You need to fix this now!",
  "rewritten_text": "you might want to please fix this when you have a chance! Thank you!",
  "emotion_analysis": {
    "emotion": "angry",
    "confidence": 0.4740,
    "all_emotions": { ... }
  },
  "target_tone": "polite",
  "confidence": 1.0,
  "suggestions": ["Alternative suggestion 1", "Alternative suggestion 2"]
}
```

#### Health Check
```bash
curl "http://localhost:5173/health"
```

### WebSocket API

Connect to `ws://localhost:5173/ws/{client_id}` for real-time communication:

```javascript
const ws = new WebSocket('ws://localhost:5173/ws/client123');

// Analyze emotion
ws.send(JSON.stringify({
  type: 'analyze_emotion',
  text: 'This is amazing!'
}));

// Rewrite text
ws.send(JSON.stringify({
  type: 'rewrite_text',
  text: 'You need to fix this now!',
  target_tone: 'polite'
}));

// Handle responses
ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  if (data.type === 'emotion_analysis') {
    console.log('Detected emotion:', data.emotion_analysis.emotion);
  } else if (data.type === 'rewrite_result') {
    console.log('Rewritten text:', data.rewritten_text);
  }
};
```

## 🎨 Supported Tones

- **Polite**: Courteous and respectful language
- **Professional**: Formal business communication
- **Friendly**: Warm and approachable tone
- **Casual**: Relaxed and informal style
- **Formal**: Very formal and precise language
- **Enthusiastic**: Excited and energetic tone
- **Empathetic**: Understanding and compassionate
- **Confident**: Assertive and self-assured
- **Humble**: Modest and respectful
- **Urgent**: Direct and time-sensitive

## 🧠 Supported Emotions

- Happy, Sad, Angry, Fearful
- Surprised, Disgusted, Neutral
- Sarcasm, Excited, Frustrated

## 🛠️ Development

### Project Structure

```
toneshiftai2/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application with WebSocket support
│   ├── models.py            # Pydantic models and data structures
│   ├── emotion_analyzer.py  # AI-powered emotion analysis
│   └── tone_rewriter.py     # Rule-based tone rewriting engine
├── pyproject.toml           # Project dependencies and configuration
├── run.py                   # Application startup script
├── setup.py                 # Easy setup script
├── demo.py                  # Interactive demo script
├── test_app.py              # Test suite
├── env.example              # Environment variables template
├── QUICKSTART.md            # Quick start guide
└── README.md                # This file
```

### Demo Script

Try the interactive demo to see all features:

```bash
uv run python demo.py
```

The demo includes:
- Emotion analysis examples
- Tone rewriting demonstrations
- Combined analysis and rewriting
- Interactive menu system

### Adding New Tones

1. Add the tone to `ToneType` enum in `models.py`
2. Add tone rules in `_get_tone_rules()` method in `tone_rewriter.py`
3. Add tone instructions in `_get_tone_instructions()` method

### Adding New Emotions

1. Add the emotion to `EmotionType` enum in `models.py`
2. Update emotion detection logic in `emotion_analyzer.py`
3. Add emotion-specific suggestions in `get_tone_suggestions()`

## 🔧 Configuration

Environment variables (see `env.example`):

- `DEBUG`: Enable debug mode (default: True)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5173)
- `MODEL_CACHE_DIR`: Directory for model cache (default: ./models)
- `MAX_TEXT_LENGTH`: Maximum text length (default: 1000)

### Quick Configuration

```bash
# Copy environment template
cp env.example .env

# Edit configuration
nano .env
```

## 📊 Performance

- **Model Loading**: ~30-60 seconds on first startup
- **Emotion Analysis**: ~1-3 seconds per request
- **Text Rewriting**: ~0.1-0.5 seconds per request (rule-based)
- **Memory Usage**: ~2-4GB RAM (depending on models)
- **Concurrent Users**: Supports multiple simultaneous users
- **Response Time**: Sub-second response times for most operations

## 🚨 Troubleshooting

### Common Issues

1. **Models not loading**: Ensure you have enough RAM (4GB+ recommended)
2. **CUDA errors**: The app will fallback to CPU if CUDA is not available
3. **Port already in use**: Change the PORT in your .env file (default: 5173)
4. **Slow performance**: Consider using a GPU for faster inference
5. **WebSocket connection issues**: Check firewall settings and ensure port is accessible
6. **Frontend errors**: Check browser console for JavaScript errors

### Quick Fixes

```bash
# Kill existing processes
pkill -f "python run.py"

# Change port if needed
echo "PORT=8000" >> .env

# Check if port is available
netstat -tulpn | grep :5173

# Restart with debug logging
DEBUG=True uv run python run.py
```

### Logs

Check the console output for detailed logs. Set `DEBUG=True` in your `.env` file for verbose logging.

### Testing

```bash
# Run tests
uv run python test_app.py

# Test API endpoints
curl http://localhost:5173/health
curl -X POST http://localhost:5173/analyze -H "Content-Type: application/json" -d '{"text": "test"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆕 Recent Updates

### Version 0.1.0 (Current)

- ✅ **Fixed emotion mapping**: Resolved Pydantic validation errors with proper emotion enum mapping
- ✅ **Improved frontend**: Added robust error handling and null checks for DOM elements
- ✅ **Enhanced rewriting**: Implemented advanced rule-based tone transformation system
- ✅ **Better performance**: Optimized text rewriting to sub-second response times
- ✅ **Comprehensive testing**: Added test suite and demo script
- ✅ **Documentation**: Complete API documentation with examples

### What's Working

- 🎭 **Emotion Analysis**: Detects 10+ emotions with confidence scores
- 🎨 **Tone Rewriting**: 10+ tone styles with intelligent pattern matching
- ⚡ **Real-time Updates**: WebSocket support for instant feedback
- 🌐 **Web Interface**: Modern, responsive UI with error handling
- 🔧 **Easy Setup**: One-command installation and startup

## 🙏 Acknowledgments

- [Transformers](https://huggingface.co/transformers/) library for emotion analysis
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [uv](https://docs.astral.sh/uv/) for fast Python package management
- [Hugging Face](https://huggingface.co/) for pre-trained models

---

**Made with ❤️ by ToneShift AI**

*Ready to transform your communication? Start the app and try it out!* 🚀
