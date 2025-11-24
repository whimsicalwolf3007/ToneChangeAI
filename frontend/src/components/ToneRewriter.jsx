import { useState } from 'react';
import { RefreshCw, Copy, Check } from 'lucide-react';
import { rewriteText } from '../services/api';
import { toneDescriptions, capitalizeFirst } from '../utils/helpers';
import './ToneRewriter.css';

const ToneRewriter = ({ inputText }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [selectedTone, setSelectedTone] = useState('polite');
  const [copied, setCopied] = useState(false);

  const tones = Object.keys(toneDescriptions);

  const handleRewrite = async () => {
    if (!inputText || inputText.trim().length === 0) {
      setError('Please enter some text to rewrite');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await rewriteText(inputText, selectedTone, true);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to rewrite text');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (result?.rewritten_text) {
      navigator.clipboard.writeText(result.rewritten_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="tone-rewriter">
      <div className="rewriter-header">
        <RefreshCw className="icon" />
        <h2>Tone Rewriter</h2>
      </div>

      <div className="tone-selector">
        <label htmlFor="tone-select">Select Target Tone:</label>
        <select 
          id="tone-select"
          value={selectedTone}
          onChange={(e) => setSelectedTone(e.target.value)}
          disabled={loading}
        >
          {tones.map(tone => (
            <option key={tone} value={tone}>
              {capitalizeFirst(tone)}
            </option>
          ))}
        </select>
        <p className="tone-description">
          {toneDescriptions[selectedTone]}
        </p>
      </div>

      <button 
        className="rewrite-btn"
        onClick={handleRewrite}
        disabled={loading || !inputText}
      >
        {loading ? 'Rewriting...' : 'Rewrite Text'}
      </button>

      {error && (
        <div className="error-message">
          <span>{error}</span>
        </div>
      )}

      {result && (
        <div className="rewrite-results">
          <div className="text-comparison">
            <div className="text-box original">
              <div className="text-box-header">
                <h4>Original Text</h4>
              </div>
              <p>{result.original_text}</p>
            </div>

            <div className="text-box rewritten">
              <div className="text-box-header">
                <h4>Rewritten ({capitalizeFirst(result.target_tone)})</h4>
                <button 
                  className="copy-btn"
                  onClick={handleCopy}
                  title="Copy to clipboard"
                >
                  {copied ? <Check className="icon" /> : <Copy className="icon" />}
                </button>
              </div>
              <p>{result.rewritten_text}</p>
            </div>
          </div>

          {result.suggestions && result.suggestions.length > 0 && (
            <div className="alternatives">
              <h4>Alternative Suggestions</h4>
              <div className="alternatives-list">
                {result.suggestions.map((suggestion, index) => (
                  <div key={index} className="alternative-item">
                    <span className="alternative-number">{index + 1}</span>
                    <p>{suggestion}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ToneRewriter;
