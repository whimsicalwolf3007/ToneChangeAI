"""Emotion analysis module using transformers."""

import torch
import numpy as np
from typing import Dict, List, Tuple
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    pipeline
)
import logging

logger = logging.getLogger(__name__)


class EmotionAnalyzer:
    """Emotion analysis using pre-trained transformer models."""
    
    def __init__(self, model_name: str = "j-hartmann/emotion-english-distilroberta-base"):
        """Initialize the emotion analyzer with a pre-trained model."""
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.emotion_pipeline = None
        self.sentiment_pipeline = None
        self._load_models()
    
    def _load_models(self):
        """Load the emotion and sentiment analysis models."""
        try:
            logger.info(f"Loading emotion analysis model: {self.model_name}")
            self.emotion_pipeline = pipeline(
                "text-classification",
                model=self.model_name,
                device=0 if self.device == "cuda" else -1,
                return_all_scores=True
            )
            
            # Load sentiment analysis for additional context
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if self.device == "cuda" else -1,
                return_all_scores=True
            )
            
            logger.info("Models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def analyze_emotion(self, text: str) -> Dict[str, float]:
        """Analyze emotions in the given text."""
        try:
            # Get emotion predictions
            emotion_results = self.emotion_pipeline(text)
            emotion_scores = {result['label'].lower(): result['score'] for result in emotion_results[0]}
            
            # Get sentiment predictions for additional context
            sentiment_results = self.sentiment_pipeline(text)
            sentiment_scores = {result['label'].lower(): result['score'] for result in sentiment_results[0]}
            
            # Combine and normalize scores
            combined_scores = self._combine_emotion_sentiment(emotion_scores, sentiment_scores)
            
            return combined_scores
            
        except Exception as e:
            logger.error(f"Error analyzing emotion: {e}")
            # Return neutral as fallback
            return {
                "neutral": 1.0,
                "happy": 0.0,
                "sad": 0.0,
                "angry": 0.0,
                "fearful": 0.0,
                "surprised": 0.0,
                "disgusted": 0.0,
                "sarcasm": 0.0,
                "excited": 0.0,
                "frustrated": 0.0
            }
    
    def _combine_emotion_sentiment(self, emotion_scores: Dict[str, float], sentiment_scores: Dict[str, float]) -> Dict[str, float]:
        """Combine emotion and sentiment scores intelligently."""
        # Map sentiment to emotions
        sentiment_mapping = {
            "positive": ["happy", "excited"],
            "negative": ["sad", "angry", "frustrated"],
            "neutral": ["neutral"]
        }
        
        # Map emotion model outputs to our enum values
        emotion_mapping = {
            "joy": "happy",
            "sadness": "sad",
            "anger": "angry",
            "fear": "fearful",
            "surprise": "surprised",
            "disgust": "disgusted"
        }
        
        # Convert emotion scores to our enum values
        combined = {}
        for emotion, score in emotion_scores.items():
            mapped_emotion = emotion_mapping.get(emotion, emotion)
            if mapped_emotion in ["happy", "sad", "angry", "fearful", "surprised", "disgusted", "neutral", "sarcasm", "excited", "frustrated"]:
                combined[mapped_emotion] = score
        
        # Boost emotions based on sentiment
        for sentiment, emotions in sentiment_mapping.items():
            if sentiment in sentiment_scores:
                sentiment_weight = sentiment_scores[sentiment] * 0.3  # 30% weight
                for emotion in emotions:
                    if emotion in combined:
                        combined[emotion] = min(1.0, combined[emotion] + sentiment_weight)
        
        # Detect sarcasm based on negative sentiment with positive words
        if sentiment_scores.get("negative", 0) > 0.6 and any(word in combined for word in ["happy", "excited"]):
            combined["sarcasm"] = min(1.0, combined.get("sarcasm", 0) + 0.4)
        
        # Ensure we have all required emotions
        for emotion in ["happy", "sad", "angry", "fearful", "surprised", "disgusted", "neutral", "sarcasm", "excited", "frustrated"]:
            if emotion not in combined:
                combined[emotion] = 0.0
        
        # Normalize scores
        total = sum(combined.values())
        if total > 0:
            combined = {k: v / total for k, v in combined.items()}
        
        return combined
    
    def get_primary_emotion(self, emotion_scores: Dict[str, float]) -> Tuple[str, float]:
        """Get the primary emotion and its confidence score."""
        if not emotion_scores:
            return "neutral", 0.0
        
        primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        return primary_emotion
    
    def get_tone_suggestions(self, emotion_scores: Dict[str, float]) -> List[str]:
        """Get tone suggestions based on emotion analysis."""
        suggestions = []
        
        # Get top emotions
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
        top_emotions = [emotion for emotion, score in sorted_emotions[:3] if score > 0.1]
        
        # Generate suggestions based on emotions
        emotion_suggestions = {
            "angry": ["Consider a more polite tone", "Try to be more diplomatic"],
            "sad": ["Add some empathy", "Be more supportive"],
            "happy": ["Maintain the positive energy", "Share the enthusiasm appropriately"],
            "frustrated": ["Take a step back and be patient", "Try a more constructive approach"],
            "sarcasm": ["Be more direct and clear", "Avoid sarcasm in professional communication"],
            "neutral": ["Add some personality", "Consider the emotional context"],
            "excited": ["Channel the enthusiasm appropriately", "Be mindful of the audience"],
            "fearful": ["Be more confident", "Address concerns directly"]
        }
        
        for emotion in top_emotions:
            if emotion in emotion_suggestions:
                suggestions.extend(emotion_suggestions[emotion])
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(suggestions))
