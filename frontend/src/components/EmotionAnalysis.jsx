import { useState } from 'react';
import { Activity, MessageCircle } from 'lucide-react';
import { analyzeEmotion } from '../services/api';
import { emotionColors, formatConfidence, capitalizeFirst } from '../utils/helpers';
import './EmotionAnalysis.css';

const EmotionAnalysis = ({ inputText, onAnalysisComplete }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    if (!inputText || inputText.trim().length === 0) {
      setError('Please enter some text to analyze');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await analyzeEmotion(inputText);
      setResult(data);
      onAnalysisComplete && onAnalysisComplete(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze emotion');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="emotion-analysis">
      <div className="analysis-header">
        <Activity className="icon" />
        <h2>Emotion Analysis</h2>
      </div>

      <button 
        className="analyze-btn"
        onClick={handleAnalyze}
        disabled={loading || !inputText}
      >
        {loading ? 'Analyzing...' : 'Analyze Emotion'}
      </button>

      {error && (
        <div className="error-message">
          <MessageCircle className="icon" />
          <span>{error}</span>
        </div>
      )}

      {result && (
        <div className="analysis-results">
          <div className="primary-emotion">
            <h3>Detected Emotion</h3>
            <div 
              className="emotion-badge"
              style={{ backgroundColor: emotionColors[result.emotion_analysis.emotion] }}
            >
              <span className="emotion-name">
                {capitalizeFirst(result.emotion_analysis.emotion)}
              </span>
              <span className="confidence">
                {formatConfidence(result.emotion_analysis.confidence)}
              </span>
            </div>
          </div>

          {result.emotion_analysis.all_emotions && (
            <div className="all-emotions">
              <h4>All Emotions</h4>
              <div className="emotion-bars">
                {Object.entries(result.emotion_analysis.all_emotions)
                  .sort((a, b) => b[1] - a[1])
                  .map(([emotion, score]) => (
                    <div key={emotion} className="emotion-bar-item">
                      <div className="emotion-label">
                        <span>{capitalizeFirst(emotion)}</span>
                        <span>{formatConfidence(score)}</span>
                      </div>
                      <div className="emotion-bar-bg">
                        <div 
                          className="emotion-bar-fill"
                          style={{ 
                            width: `${score * 100}%`,
                            backgroundColor: emotionColors[emotion]
                          }}
                        />
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          )}

          {result.suggestions && result.suggestions.length > 0 && (
            <div className="suggestions">
              <h4>Suggestions</h4>
              {result.suggestions.map((suggestion, index) => (
                <div key={index} className="suggestion-item">
                  {suggestion}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default EmotionAnalysis;
