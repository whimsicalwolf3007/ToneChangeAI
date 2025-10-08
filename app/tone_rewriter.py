"""Tone rewriting module using language models."""

import torch
from typing import Dict, List, Tuple
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)
import logging
import re

logger = logging.getLogger(__name__)


class ToneRewriter:
    """Rewrites text to match specific tones using language models."""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        """Initialize the tone rewriter with a language model."""
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.model = None
        self.rewrite_pipeline = None
        self._load_models()
    
    def _load_models(self):
        """Load the language model for text rewriting."""
        try:
            logger.info(f"Loading tone rewriter model: {self.model_name}")
            
            # Use a more appropriate model for text generation
            self.rewrite_pipeline = pipeline(
                "text-generation",
                model="gpt2",
                device=0 if self.device == "cuda" else -1,
                max_length=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=50256
            )
            
            logger.info("Tone rewriter model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading tone rewriter model: {e}")
            # Fallback to rule-based rewriting
            self.rewrite_pipeline = None
            logger.info("Using rule-based rewriting as fallback")
    
    def rewrite_text(self, text: str, target_tone: str, preserve_meaning: bool = True) -> Tuple[str, float]:
        """Rewrite text to match the target tone."""
        try:
            if self.rewrite_pipeline:
                return self._ai_rewrite(text, target_tone, preserve_meaning)
            else:
                return self._rule_based_rewrite(text, target_tone, preserve_meaning)
        except Exception as e:
            logger.error(f"Error rewriting text: {e}")
            return text, 0.0
    
    def _ai_rewrite(self, text: str, target_tone: str, preserve_meaning: bool) -> Tuple[str, float]:
        """Use AI model to rewrite text."""
        # For now, use rule-based rewriting as the AI model is generating poor results
        # TODO: Implement a better AI model or fine-tune the current one
        return self._rule_based_rewrite(text, target_tone, preserve_meaning)
    
    def _rule_based_rewrite(self, text: str, target_tone: str, preserve_meaning: bool) -> Tuple[str, float]:
        """Use rule-based approach to rewrite text."""
        rewritten = text
        changes_made = 0
        
        # Apply tone-specific transformations
        tone_rules = self._get_tone_rules(target_tone)
        
        # Apply rules in order of specificity (most specific first)
        for pattern, replacement in tone_rules.items():
            if pattern == r'^(.+)$':  # Skip the catch-all pattern for now
                continue
            new_text = re.sub(pattern, replacement, rewritten, flags=re.IGNORECASE)
            if new_text != rewritten:
                rewritten = new_text
                changes_made += 1
        
        # Apply catch-all pattern only if no other changes were made
        if changes_made == 0 and r'^(.+)$' in tone_rules:
            rewritten = re.sub(r'^(.+)$', tone_rules[r'^(.+)$'], rewritten, flags=re.IGNORECASE)
            changes_made += 1
        
        # Apply general politeness rules
        if target_tone in ["polite", "professional", "formal"]:
            original_rewritten = rewritten
            rewritten = self._apply_politeness_rules(rewritten)
            if rewritten != original_rewritten:
                changes_made += 1
        
        # Calculate confidence based on changes made
        confidence = min(1.0, changes_made * 0.3 + 0.4)  # Base confidence of 0.4
        
        return rewritten, confidence
    
    def _get_tone_instructions(self, target_tone: str) -> str:
        """Get specific instructions for each tone."""
        instructions = {
            "polite": "Use polite language, add please/thank you, avoid direct commands",
            "professional": "Use formal business language, be concise and clear",
            "friendly": "Use warm, approachable language, add personal touches",
            "casual": "Use informal language, contractions, and relaxed tone",
            "formal": "Use very formal language, avoid contractions, be precise",
            "enthusiastic": "Add excitement, use exclamation points, show energy",
            "empathetic": "Show understanding and compassion, acknowledge feelings",
            "confident": "Use assertive language, avoid hedging words",
            "humble": "Be modest, acknowledge others' contributions",
            "urgent": "Use direct language, emphasize time sensitivity"
        }
        return instructions.get(target_tone, "Maintain the original tone")
    
    def _get_tone_rules(self, target_tone: str) -> Dict[str, str]:
        """Get regex rules for tone transformation."""
        rules = {}
        
        if target_tone == "polite":
            rules.update({
                r'\b(you need to|you should|you must)\b': 'you might want to',
                r'\b(fix this|fix that|fix it)\b': 'please fix this',
                r'\b(now|immediately|right now)\b': 'when you have a chance',
                r'\b(no|nope|nah)\b': 'I\'m afraid not',
                r'\b(yes|yeah|yep)\b': 'yes, absolutely',
                r'^(.+)$': r'Could you please \1'  # Add polite prefix to commands
            })
        
        elif target_tone == "professional":
            rules.update({
                r'\b(yeah|yep|yup)\b': 'yes',
                r'\b(nah|nope)\b': 'no',
                r'\b(gonna|gotta|wanna)\b': 'going to/got to/want to',
                r'\b(awesome|cool|great)\b': 'excellent',
                r'\b(thanks|thx)\b': 'thank you',
                r'\b(fix this|fix that|fix it)\b': 'address this issue',
                r'\b(now|immediately|right now)\b': 'as soon as possible'
            })
        
        elif target_tone == "friendly":
            rules.update({
                r'\b(please|thank you)\b': 'thanks',
                r'\b(no problem|not a problem)\b': 'happy to help',
                r'\b(regarding|concerning)\b': 'about',
                r'\b(utilize|utilization)\b': 'use/using',
                r'\b(fix this|fix that|fix it)\b': 'take a look at this',
                r'\b(now|immediately|right now)\b': 'when you get a chance'
            })
        
        elif target_tone == "casual":
            rules.update({
                r'\b(please|thank you)\b': 'thanks',
                r'\b(utilize|utilization)\b': 'use/using',
                r'\b(regarding|concerning)\b': 'about',
                r'\b(assistance|help)\b': 'help',
                r'\b(fix this|fix that|fix it)\b': 'check this out',
                r'\b(now|immediately|right now)\b': 'when you can'
            })
        
        elif target_tone == "enthusiastic":
            rules.update({
                r'\b(good|great|nice)\b': 'amazing',
                r'\b(okay|ok)\b': 'fantastic',
                r'\b(thanks|thank you)\b': 'thank you so much',
                r'\b(fix this|fix that|fix it)\b': 'let\'s get this fixed',
                r'\b(now|immediately|right now)\b': 'right away',
                r'\.$': '!'
            })
        
        elif target_tone == "empathetic":
            rules.update({
                r'\b(fix this|fix that|fix it)\b': 'I understand this needs attention',
                r'\b(now|immediately|right now)\b': 'when you\'re ready',
                r'\b(you need to|you should|you must)\b': 'it would be helpful if',
                r'^(.+)$': r'I can see that \1'  # Add empathetic prefix
            })
        
        elif target_tone == "confident":
            rules.update({
                r'\b(fix this|fix that|fix it)\b': 'we need to resolve this',
                r'\b(now|immediately|right now)\b': 'immediately',
                r'\b(you need to|you should|you must)\b': 'we will',
                r'\b(maybe|perhaps|possibly)\b': 'definitely'
            })
        
        elif target_tone == "humble":
            rules.update({
                r'\b(fix this|fix that|fix it)\b': 'if possible, could we address this',
                r'\b(now|immediately|right now)\b': 'when convenient',
                r'\b(you need to|you should|you must)\b': 'it would be appreciated if',
                r'^(.+)$': r'If it\'s not too much trouble, \1'  # Add humble prefix
            })
        
        elif target_tone == "urgent":
            rules.update({
                r'\b(fix this|fix that|fix it)\b': 'this requires immediate attention',
                r'\b(now|immediately|right now)\b': 'ASAP',
                r'\b(you need to|you should|you must)\b': 'we must',
                r'^(.+)$': r'URGENT: \1'  # Add urgent prefix
            })
        
        return rules
    
    def _apply_politeness_rules(self, text: str) -> str:
        """Apply general politeness rules."""
        # Add please to requests
        if text.endswith('?') and not text.startswith(('please', 'could', 'would', 'may')):
            text = f"Could you please {text.lower()}"
        
        # Add thank you to responses
        if not any(word in text.lower() for word in ['thank', 'thanks', 'appreciate']):
            text = f"{text} Thank you!"
        
        return text
    
    def _clean_generated_text(self, text: str) -> str:
        """Clean up generated text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove incomplete sentences at the end
        if text and not text[-1] in '.!?':
            sentences = text.split('.')
            if len(sentences) > 1:
                text = '.'.join(sentences[:-1]) + '.'
        
        # Remove any remaining prompt text
        text = re.sub(r'^(Original:|Rewritten:).*', '', text).strip()
        
        return text
    
    def get_alternative_suggestions(self, text: str, target_tone: str) -> List[str]:
        """Get alternative suggestions for the rewritten text."""
        suggestions = []
        
        # Generate multiple variations
        for i in range(3):
            try:
                rewritten, _ = self.rewrite_text(text, target_tone, preserve_meaning=True)
                if rewritten and rewritten != text:
                    suggestions.append(rewritten)
            except Exception as e:
                logger.error(f"Error generating suggestion {i}: {e}")
                continue
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(suggestions))
