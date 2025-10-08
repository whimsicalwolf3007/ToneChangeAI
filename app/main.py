"""Main FastAPI application for ToneShift AI."""

import os
import time
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from .models import (
    RewriteRequest, RewriteResponse, AnalysisRequest, AnalysisResponse,
    HealthResponse, EmotionType, ToneType
)
from .emotion_analyzer import EmotionAnalyzer
from .tone_rewriter import ToneRewriter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for models
emotion_analyzer = None
tone_rewriter = None
start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - load models on startup."""
    global emotion_analyzer, tone_rewriter
    
    logger.info("Starting ToneShift AI application...")
    
    try:
        # Initialize models
        logger.info("Loading emotion analyzer...")
        emotion_analyzer = EmotionAnalyzer()
        
        logger.info("Loading tone rewriter...")
        tone_rewriter = ToneRewriter()
        
        logger.info("All models loaded successfully!")
        yield
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        logger.info("Shutting down ToneShift AI application...")


# Create FastAPI app
app = FastAPI(
    title="ToneShift AI",
    description="Emotion-Aware Real-Time Chat Rewriter",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected")

    async def send_personal_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to {client_id}: {e}")
                self.disconnect(client_id)

    async def broadcast(self, message: dict):
        for client_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {client_id}: {e}")
                self.disconnect(client_id)


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main application page."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ToneShift AI - Emotion-Aware Chat Rewriter</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                padding: 2rem;
                max-width: 800px;
                width: 90%;
            }
            .header {
                text-align: center;
                margin-bottom: 2rem;
            }
            .header h1 {
                color: #333;
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
            }
            .header p {
                color: #666;
                font-size: 1.1rem;
            }
            .input-section {
                margin-bottom: 2rem;
            }
            .input-group {
                margin-bottom: 1rem;
            }
            label {
                display: block;
                margin-bottom: 0.5rem;
                font-weight: 600;
                color: #333;
            }
            textarea, select {
                width: 100%;
                padding: 1rem;
                border: 2px solid #e1e5e9;
                border-radius: 10px;
                font-size: 1rem;
                transition: border-color 0.3s;
            }
            textarea:focus, select:focus {
                outline: none;
                border-color: #667eea;
            }
            textarea {
                resize: vertical;
                min-height: 120px;
            }
            .button-group {
                display: flex;
                gap: 1rem;
                margin-top: 1rem;
            }
            button {
                flex: 1;
                padding: 1rem;
                border: none;
                border-radius: 10px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            }
            .analyze-btn {
                background: #667eea;
                color: white;
            }
            .analyze-btn:hover {
                background: #5a6fd8;
                transform: translateY(-2px);
            }
            .rewrite-btn {
                background: #764ba2;
                color: white;
            }
            .rewrite-btn:hover {
                background: #6a4190;
                transform: translateY(-2px);
            }
            .results {
                margin-top: 2rem;
                padding: 1.5rem;
                background: #f8f9fa;
                border-radius: 10px;
                display: none;
            }
            .emotion-display {
                display: flex;
                gap: 1rem;
                margin-bottom: 1rem;
                flex-wrap: wrap;
            }
            .emotion-tag {
                padding: 0.5rem 1rem;
                background: #667eea;
                color: white;
                border-radius: 20px;
                font-size: 0.9rem;
                font-weight: 500;
            }
            .rewritten-text {
                background: white;
                padding: 1rem;
                border-radius: 10px;
                border-left: 4px solid #764ba2;
                margin-top: 1rem;
            }
            .suggestions {
                margin-top: 1rem;
            }
            .suggestion {
                background: white;
                padding: 0.8rem;
                margin: 0.5rem 0;
                border-radius: 8px;
                border-left: 3px solid #667eea;
            }
            .loading {
                text-align: center;
                color: #666;
                font-style: italic;
            }
            .error {
                background: #fee;
                color: #c33;
                padding: 1rem;
                border-radius: 10px;
                margin-top: 1rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎭 ToneShift AI</h1>
                <p>Transform your messages with emotion-aware tone rewriting</p>
            </div>
            
            <div class="input-section">
                <div class="input-group">
                    <label for="textInput">Enter your message:</label>
                    <textarea id="textInput" placeholder="Type your message here..."></textarea>
                </div>
                
                <div class="input-group">
                    <label for="toneSelect">Choose target tone:</label>
                    <select id="toneSelect">
                        <option value="polite">Polite</option>
                        <option value="professional">Professional</option>
                        <option value="friendly">Friendly</option>
                        <option value="casual">Casual</option>
                        <option value="formal">Formal</option>
                        <option value="enthusiastic">Enthusiastic</option>
                        <option value="empathetic">Empathetic</option>
                        <option value="confident">Confident</option>
                        <option value="humble">Humble</option>
                        <option value="urgent">Urgent</option>
                    </select>
                </div>
                
                <div class="button-group">
                    <button class="analyze-btn" onclick="analyzeEmotion()">Analyze Emotion</button>
                    <button class="rewrite-btn" onclick="rewriteText()">Rewrite Text</button>
                </div>
            </div>
            
            <div id="results" class="results">
                <div id="emotionResults"></div>
                <div id="rewriteResults"></div>
                <div id="suggestions"></div>
            </div>
        </div>

        <script>
            let ws = null;
            let clientId = Math.random().toString(36).substr(2, 9);
            
            function connectWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                ws = new WebSocket(`${protocol}//${window.location.host}/ws/${clientId}`);
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    handleWebSocketMessage(data);
                };
                
                ws.onclose = function() {
                    console.log('WebSocket disconnected');
                    setTimeout(connectWebSocket, 3000);
                };
            }
            
            function handleWebSocketMessage(data) {
                try {
                    if (data.type === 'emotion_analysis') {
                        displayEmotionResults(data);
                    } else if (data.type === 'rewrite_result') {
                        displayRewriteResults(data);
                    } else if (data.type === 'error') {
                        showError(data.message);
                    } else {
                        console.log('Unknown WebSocket message type:', data.type);
                    }
                } catch (error) {
                    console.error('Error handling WebSocket message:', error);
                    showError('Error processing response: ' + error.message);
                }
            }
            
            async function analyzeEmotion() {
                const text = document.getElementById('textInput').value.trim();
                if (!text) {
                    alert('Please enter some text to analyze');
                    return;
                }
                
                showLoading('Analyzing emotions...');
                
                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text: text })
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || `HTTP ${response.status}`);
                    }
                    
                    const data = await response.json();
                    displayEmotionResults(data);
                } catch (error) {
                    console.error('Error analyzing emotion:', error);
                    showError('Error analyzing emotion: ' + error.message);
                }
            }
            
            async function rewriteText() {
                const text = document.getElementById('textInput').value.trim();
                const tone = document.getElementById('toneSelect').value;
                
                if (!text) {
                    alert('Please enter some text to rewrite');
                    return;
                }
                
                showLoading('Rewriting text...');
                
                try {
                    const response = await fetch('/rewrite', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            text: text, 
                            target_tone: tone,
                            preserve_meaning: true 
                        })
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || `HTTP ${response.status}`);
                    }
                    
                    const data = await response.json();
                    displayRewriteResults(data);
                } catch (error) {
                    console.error('Error rewriting text:', error);
                    showError('Error rewriting text: ' + error.message);
                }
            }
            
            function displayEmotionResults(data) {
                const resultsDiv = document.getElementById('results');
                const emotionDiv = document.getElementById('emotionResults');
                
                if (!resultsDiv) {
                    console.error('Results div not found');
                    return;
                }
                
                if (!emotionDiv) {
                    console.error('Emotion results div not found');
                    return;
                }
                
                resultsDiv.style.display = 'block';
                
                // Handle both direct API response and WebSocket response
                const emotionAnalysis = data.emotion_analysis || data;
                const primaryEmotion = emotionAnalysis.emotion;
                const confidence = ((emotionAnalysis.confidence || 0) * 100).toFixed(1);
                
                emotionDiv.innerHTML = `
                    <h3>Emotion Analysis</h3>
                    <div class="emotion-display">
                        <div class="emotion-tag" style="background: #667eea;">
                            ${primaryEmotion.charAt(0).toUpperCase() + primaryEmotion.slice(1)} (${confidence}%)
                        </div>
                    </div>
                `;
                
                if (data.suggestions && data.suggestions.length > 0) {
                    const suggestionsDiv = document.getElementById('suggestions');
                    if (suggestionsDiv) {
                        suggestionsDiv.innerHTML = `
                            <h4>Suggestions:</h4>
                            ${data.suggestions.map(s => `<div class="suggestion">${s}</div>`).join('')}
                        `;
                    }
                }
            }
            
            function displayRewriteResults(data) {
                const resultsDiv = document.getElementById('results');
                const rewriteDiv = document.getElementById('rewriteResults');
                
                resultsDiv.style.display = 'block';
                
                // Ensure rewriteDiv exists
                if (!rewriteDiv) {
                    console.error('rewriteResults div not found');
                    return;
                }
                
                rewriteDiv.innerHTML = `
                    <h3>Rewritten Text</h3>
                    <div class="rewritten-text">
                        <strong>Original:</strong> ${data.original_text}<br><br>
                        <strong>Rewritten (${data.target_tone}):</strong> ${data.rewritten_text}
                    </div>
                `;
                
                if (data.suggestions && data.suggestions.length > 0) {
                    const suggestionsDiv = document.getElementById('suggestions');
                    if (suggestionsDiv) {
                        suggestionsDiv.innerHTML = `
                            <h4>Alternative Suggestions:</h4>
                            ${data.suggestions.map(s => `<div class="suggestion">${s}</div>`).join('')}
                        `;
                    }
                }
            }
            
            function showLoading(message) {
                const resultsDiv = document.getElementById('results');
                if (!resultsDiv) {
                    console.error('Results div not found for loading display');
                    return;
                }
                resultsDiv.style.display = 'block';
                resultsDiv.innerHTML = `<div class="loading">${message}</div>`;
            }
            
            function showError(message) {
                const resultsDiv = document.getElementById('results');
                if (!resultsDiv) {
                    console.error('Results div not found for error display');
                    alert('Error: ' + message);
                    return;
                }
                resultsDiv.style.display = 'block';
                resultsDiv.innerHTML = `<div class="error">${message}</div>`;
            }
            
            // Connect WebSocket on page load
            connectWebSocket();
        </script>
    </body>
    </html>
    """


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time communication."""
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            await handle_websocket_message(data, client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {e}")
        manager.disconnect(client_id)


async def handle_websocket_message(data: dict, client_id: str):
    """Handle incoming WebSocket messages."""
    try:
        message_type = data.get("type")
        
        if message_type == "analyze_emotion":
            text = data.get("text", "")
            if not text:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "No text provided for analysis"
                }, client_id)
                return
            
            # Analyze emotion
            emotion_scores = emotion_analyzer.analyze_emotion(text)
            primary_emotion, confidence = emotion_analyzer.get_primary_emotion(emotion_scores)
            suggestions = emotion_analyzer.get_tone_suggestions(emotion_scores)
            
            await manager.send_personal_message({
                "type": "emotion_analysis",
                "emotion_analysis": {
                    "emotion": primary_emotion,
                    "confidence": confidence,
                    "all_emotions": emotion_scores
                },
                "suggestions": suggestions
            }, client_id)
        
        elif message_type == "rewrite_text":
            text = data.get("text", "")
            target_tone = data.get("target_tone", "polite")
            
            if not text:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "No text provided for rewriting"
                }, client_id)
                return
            
            # Analyze emotion first
            emotion_scores = emotion_analyzer.analyze_emotion(text)
            primary_emotion, confidence = emotion_analyzer.get_primary_emotion(emotion_scores)
            
            # Rewrite text
            rewritten_text, rewrite_confidence = tone_rewriter.rewrite_text(
                text, target_tone, preserve_meaning=True
            )
            
            # Get alternative suggestions
            suggestions = tone_rewriter.get_alternative_suggestions(text, target_tone)
            
            await manager.send_personal_message({
                "type": "rewrite_result",
                "original_text": text,
                "rewritten_text": rewritten_text,
                "emotion_analysis": {
                    "emotion": primary_emotion,
                    "confidence": confidence,
                    "all_emotions": emotion_scores
                },
                "target_tone": target_tone,
                "confidence": rewrite_confidence,
                "suggestions": suggestions
            }, client_id)
        
        else:
            await manager.send_personal_message({
                "type": "error",
                "message": f"Unknown message type: {message_type}"
            }, client_id)
    
    except Exception as e:
        logger.error(f"Error handling WebSocket message: {e}")
        await manager.send_personal_message({
            "type": "error",
            "message": f"Internal server error: {str(e)}"
        }, client_id)


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_emotion(request: AnalysisRequest):
    """Analyze emotion in the provided text."""
    try:
        if not emotion_analyzer:
            raise HTTPException(status_code=503, detail="Emotion analyzer not loaded")
        
        # Analyze emotion
        emotion_scores = emotion_analyzer.analyze_emotion(request.text)
        primary_emotion, confidence = emotion_analyzer.get_primary_emotion(emotion_scores)
        suggestions = emotion_analyzer.get_tone_suggestions(emotion_scores)
        
        return AnalysisResponse(
            text=request.text,
            emotion_analysis={
                "emotion": primary_emotion,
                "confidence": confidence,
                "all_emotions": emotion_scores
            },
            suggestions=suggestions
        )
    
    except Exception as e:
        logger.error(f"Error analyzing emotion: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing emotion: {str(e)}")


@app.post("/rewrite", response_model=RewriteResponse)
async def rewrite_text(request: RewriteRequest):
    """Rewrite text with the specified tone."""
    try:
        if not emotion_analyzer or not tone_rewriter:
            raise HTTPException(status_code=503, detail="Models not loaded")
        
        # Analyze emotion first
        emotion_scores = emotion_analyzer.analyze_emotion(request.text)
        primary_emotion, confidence = emotion_analyzer.get_primary_emotion(emotion_scores)
        
        # Rewrite text
        rewritten_text, rewrite_confidence = tone_rewriter.rewrite_text(
            request.text, request.target_tone, request.preserve_meaning
        )
        
        # Get alternative suggestions
        suggestions = tone_rewriter.get_alternative_suggestions(request.text, request.target_tone)
        
        return RewriteResponse(
            original_text=request.text,
            rewritten_text=rewritten_text,
            emotion_analysis={
                "emotion": primary_emotion,
                "confidence": confidence,
                "all_emotions": emotion_scores
            },
            target_tone=request.target_tone,
            confidence=rewrite_confidence,
            suggestions=suggestions
        )
    
    except Exception as e:
        logger.error(f"Error rewriting text: {e}")
        raise HTTPException(status_code=500, detail=f"Error rewriting text: {str(e)}")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    uptime = time.time() - start_time
    models_loaded = emotion_analyzer is not None and tone_rewriter is not None
    
    return HealthResponse(
        status="healthy" if models_loaded else "degraded",
        version="0.1.0",
        models_loaded=models_loaded,
        uptime=uptime
    )


@app.get("/api/emotions")
async def get_available_emotions():
    """Get list of available emotion types."""
    return {"emotions": [e.value for e in EmotionType]}


@app.get("/api/tones")
async def get_available_tones():
    """Get list of available tone types."""
    return {"tones": [t.value for t in ToneType]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
