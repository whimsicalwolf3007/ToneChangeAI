#!/usr/bin/env python3
"""Demo script for ToneShift AI."""

import asyncio
import json
import time
from app.emotion_analyzer import EmotionAnalyzer
from app.tone_rewriter import ToneRewriter

async def demo_emotion_analysis():
    """Demo emotion analysis functionality."""
    print("🎭 ToneShift AI Demo - Emotion Analysis")
    print("=" * 50)
    
    # Initialize analyzer
    print("🔄 Loading emotion analyzer...")
    analyzer = EmotionAnalyzer()
    
    # Test cases
    test_cases = [
        "This is absolutely amazing! I love it!",
        "I'm so frustrated with this situation.",
        "That's a great idea, thanks for sharing.",
        "I can't believe you did that...",
        "I'm really excited about the new project!",
        "This is terrible, I hate it.",
        "Sure, whatever you say...",
        "I'm really worried about the deadline.",
        "Congratulations on your promotion!",
        "I'm not sure about this approach."
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: \"{text}\"")
        
        # Analyze emotion
        emotion_scores = analyzer.analyze_emotion(text)
        primary_emotion, confidence = analyzer.get_primary_emotion(emotion_scores)
        suggestions = analyzer.get_tone_suggestions(emotion_scores)
        
        print(f"🎯 Primary Emotion: {primary_emotion.upper()} ({confidence:.2%} confidence)")
        print(f"📊 All Emotions: {json.dumps(emotion_scores, indent=2)}")
        if suggestions:
            print(f"💡 Suggestions: {', '.join(suggestions)}")
        
        time.sleep(1)  # Pause for readability

async def demo_tone_rewriting():
    """Demo tone rewriting functionality."""
    print("\n\n🎨 ToneShift AI Demo - Tone Rewriting")
    print("=" * 50)
    
    # Initialize rewriter
    print("🔄 Loading tone rewriter...")
    rewriter = ToneRewriter()
    
    # Test cases
    test_cases = [
        ("You need to fix this bug immediately!", "polite"),
        ("This is a terrible idea.", "professional"),
        ("I don't like this approach.", "friendly"),
        ("We should probably consider other options.", "confident"),
        ("This won't work at all.", "empathetic"),
        ("The deadline is tomorrow.", "urgent"),
        ("I think we need to discuss this.", "casual"),
        ("This is unacceptable.", "humble"),
        ("We need to act now.", "enthusiastic"),
        ("This is not good enough.", "formal")
    ]
    
    for i, (text, target_tone) in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: \"{text}\"")
        print(f"🎯 Target Tone: {target_tone.upper()}")
        
        # Rewrite text
        rewritten, confidence = rewriter.rewrite_text(text, target_tone, preserve_meaning=True)
        suggestions = rewriter.get_alternative_suggestions(text, target_tone)
        
        print(f"✨ Rewritten: \"{rewritten}\"")
        print(f"📊 Confidence: {confidence:.2%}")
        if suggestions:
            print(f"💡 Alternatives: {suggestions[:2]}")  # Show first 2 suggestions
        
        time.sleep(1)  # Pause for readability

async def demo_combined():
    """Demo combined emotion analysis and tone rewriting."""
    print("\n\n🚀 ToneShift AI Demo - Combined Analysis & Rewriting")
    print("=" * 60)
    
    # Initialize both
    print("🔄 Loading models...")
    analyzer = EmotionAnalyzer()
    rewriter = ToneRewriter()
    
    # Complex test cases
    test_cases = [
        ("I'm really frustrated with this bug that keeps happening!", "polite"),
        ("This is the worst code I've ever seen.", "professional"),
        ("I can't believe you forgot the meeting again.", "empathetic"),
        ("This project is going to fail spectacularly.", "confident"),
        ("I'm so excited about this new feature!", "formal"),
        ("That's a stupid idea and it won't work.", "friendly"),
        ("We're running out of time and nothing is working.", "urgent"),
        ("I'm not sure if this is the right approach.", "enthusiastic"),
        ("This is completely wrong and needs to be fixed.", "humble"),
        ("I'm really worried about the quality of this work.", "casual")
    ]
    
    for i, (text, target_tone) in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: \"{text}\"")
        print(f"🎯 Target Tone: {target_tone.upper()}")
        
        # Analyze emotion
        emotion_scores = analyzer.analyze_emotion(text)
        primary_emotion, emotion_confidence = analyzer.get_primary_emotion(emotion_scores)
        
        # Rewrite text
        rewritten, rewrite_confidence = rewriter.rewrite_text(text, target_tone, preserve_meaning=True)
        
        print(f"🎭 Detected Emotion: {primary_emotion.upper()} ({emotion_confidence:.2%})")
        print(f"✨ Rewritten: \"{rewritten}\"")
        print(f"📊 Rewrite Confidence: {rewrite_confidence:.2%}")
        
        time.sleep(1)  # Pause for readability

async def main():
    """Main demo function."""
    print("🎭 Welcome to ToneShift AI Demo!")
    print("This demo showcases the emotion analysis and tone rewriting capabilities.")
    print("\nChoose a demo to run:")
    print("1. Emotion Analysis Only")
    print("2. Tone Rewriting Only") 
    print("3. Combined Analysis & Rewriting")
    print("4. Run All Demos")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            await demo_emotion_analysis()
        elif choice == "2":
            await demo_tone_rewriting()
        elif choice == "3":
            await demo_combined()
        elif choice == "4":
            await demo_emotion_analysis()
            await demo_tone_rewriting()
            await demo_combined()
        else:
            print("Invalid choice. Running all demos...")
            await demo_emotion_analysis()
            await demo_tone_rewriting()
            await demo_combined()
        
        print("\n\n🎉 Demo completed!")
        print("🚀 To run the full web application, use: uv run python run.py")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
