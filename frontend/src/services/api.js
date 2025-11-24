import axios from 'axios';

const API_BASE_URL = '/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Analyze emotion in text
export const analyzeEmotion = async (text) => {
  try {
    const response = await api.post('/analyze', { text });
    return response.data;
  } catch (error) {
    console.error('Error analyzing emotion:', error);
    throw error;
  }
};

// Rewrite text with target tone
export const rewriteText = async (text, targetTone, preserveMeaning = true) => {
  try {
    const response = await api.post('/rewrite', {
      text,
      target_tone: targetTone,
      preserve_meaning: preserveMeaning,
    });
    return response.data;
  } catch (error) {
    console.error('Error rewriting text:', error);
    throw error;
  }
};

// Get health status
export const getHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};

// Get available emotions
export const getAvailableEmotions = async () => {
  try {
    const response = await axios.get('http://localhost:5173/api/emotions');
    return response.data;
  } catch (error) {
    console.error('Error getting emotions:', error);
    throw error;
  }
};

// Get available tones
export const getAvailableTones = async () => {
  try {
    const response = await axios.get('http://localhost:5173/api/tones');
    return response.data;
  } catch (error) {
    console.error('Error getting tones:', error);
    throw error;
  }
};

// WebSocket connection class
export class WebSocketClient {
  constructor(clientId, onMessage, onError) {
    this.clientId = clientId;
    this.onMessage = onMessage;
    this.onError = onError;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/${this.clientId}`;

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.onMessage(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
          this.onError && this.onError(error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.onError && this.onError(error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.attemptReconnect();
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.onError && this.onError(error);
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      setTimeout(() => this.connect(), 3000);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.error('WebSocket is not connected');
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export default api;
