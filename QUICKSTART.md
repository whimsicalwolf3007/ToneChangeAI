# 🚀 ToneShift AI - Quick Start Guide

## Get Started in 3 Steps

### 1. Install Dependencies
```bash
uv sync
```

### 2. Start the Application
```bash
uv run python run.py
```

### 3. Open Your Browser
Navigate to: `http://localhost:8000`

## 🎯 What You Can Do

### Real-Time Emotion Analysis
- Type any message and click "Analyze Emotion"
- See detected emotions like happy, sad, angry, sarcastic, etc.
- Get confidence scores and suggestions

### Intelligent Tone Rewriting
- Choose from 10+ tone styles (polite, professional, friendly, etc.)
- Transform "You need to fix this!" → "Could you please fix this?"
- Get alternative suggestions for each rewrite

### WebSocket API
- Real-time communication for instant feedback
- Perfect for chat applications and integrations

## 🧪 Try the Demo

Run the interactive demo to see all features:
```bash
uv run python demo.py
```

## 📡 API Examples

### Analyze Emotion
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!"}'
```

### Rewrite Text
```bash
curl -X POST "http://localhost:8000/rewrite" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "You need to fix this now!",
    "target_tone": "polite"
  }'
```

## 🎨 Supported Tones

- **Polite**: Courteous and respectful
- **Professional**: Formal business language
- **Friendly**: Warm and approachable
- **Casual**: Relaxed and informal
- **Formal**: Very formal and precise
- **Enthusiastic**: Excited and energetic
- **Empathetic**: Understanding and compassionate
- **Confident**: Assertive and self-assured
- **Humble**: Modest and respectful
- **Urgent**: Direct and time-sensitive

## 🧠 Detected Emotions

- Happy, Sad, Angry, Fearful
- Surprised, Disgusted, Neutral
- Sarcasm, Excited, Frustrated

## 🔧 Configuration

Edit `.env` file to customize:
- `DEBUG=True` - Enable debug mode
- `HOST=0.0.0.0` - Server host
- `PORT=8000` - Server port
- `MAX_TEXT_LENGTH=1000` - Max text length

## 🚨 Troubleshooting

- **Models loading slowly?** This is normal on first run (30-60 seconds)
- **Out of memory?** Ensure you have 4GB+ RAM available
- **Port in use?** Change `PORT` in `.env` file

## 📚 Full Documentation

See `README.md` for complete documentation and advanced usage.

---

**Ready to transform your communication? Start the app and try it out!** 🎭✨
