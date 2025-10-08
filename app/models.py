"""Pydantic models for the ToneShift AI application."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class EmotionType(str, Enum):
    """Supported emotion types for analysis."""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEARFUL = "fearful"
    SURPRISED = "surprised"
    DISGUSTED = "disgusted"
    NEUTRAL = "neutral"
    SARCASM = "sarcasm"
    EXCITED = "excited"
    FRUSTRATED = "frustrated"


class ToneType(str, Enum):
    """Supported tone types for rewriting."""
    POLITE = "polite"
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    CASUAL = "casual"
    FORMAL = "formal"
    ENTHUSIASTIC = "enthusiastic"
    EMPATHETIC = "empathetic"
    CONFIDENT = "confident"
    HUMBLE = "humble"
    URGENT = "urgent"


class EmotionAnalysis(BaseModel):
    """Emotion analysis result."""
    emotion: EmotionType
    confidence: float = Field(ge=0.0, le=1.0)
    all_emotions: Dict[str, float] = Field(description="Confidence scores for all emotions")


class RewriteRequest(BaseModel):
    """Request to rewrite text with specific tone."""
    text: str = Field(..., min_length=1, max_length=1000, description="Text to rewrite")
    target_tone: ToneType = Field(..., description="Desired tone for the rewritten text")
    preserve_meaning: bool = Field(True, description="Whether to preserve the original meaning")
    context: Optional[str] = Field(None, max_length=500, description="Additional context for better rewriting")


class RewriteResponse(BaseModel):
    """Response containing rewritten text and analysis."""
    original_text: str
    rewritten_text: str
    emotion_analysis: EmotionAnalysis
    target_tone: ToneType
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the rewrite quality")
    suggestions: List[str] = Field(default_factory=list, description="Alternative suggestions")


class AnalysisRequest(BaseModel):
    """Request to analyze emotion in text."""
    text: str = Field(..., min_length=1, max_length=1000, description="Text to analyze")


class AnalysisResponse(BaseModel):
    """Response containing emotion analysis."""
    text: str
    emotion_analysis: EmotionAnalysis
    suggestions: List[str] = Field(default_factory=list, description="Tone suggestions based on analysis")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    models_loaded: bool
    uptime: float
