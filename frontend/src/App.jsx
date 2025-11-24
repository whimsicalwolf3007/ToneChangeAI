import { useState } from 'react';
import { MessageSquare, Brain } from 'lucide-react';
import EmotionAnalysis from './components/EmotionAnalysis';
import ToneRewriter from './components/ToneRewriter';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');

  return (
    <div className="app">
      <div className="app-background"></div>
      
      <div className="app-container">
        <header className="app-header">
          <div className="header-content">
            <Brain className="logo-icon" />
            <div className="header-text">
              <h1>🎭 ToneShift AI</h1>
              <p>Transform your messages with emotion-aware tone rewriting</p>
            </div>
          </div>
        </header>

        <main className="app-main">
          <div className="input-section">
            <div className="input-header">
              <MessageSquare className="icon" />
              <h2>Enter Your Message</h2>
            </div>
            <textarea
              className="text-input"
              placeholder="Type or paste your message here..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              rows={6}
              maxLength={1000}
            />
            <div className="char-counter">
              {inputText.length} / 1000 characters
            </div>
          </div>

          <div className="features-grid">
            <EmotionAnalysis inputText={inputText} />
            <ToneRewriter inputText={inputText} />
          </div>
        </main>

        <footer className="app-footer">
          <p>Made with ❤️ by ToneShift AI | Powered by FastAPI & React</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
