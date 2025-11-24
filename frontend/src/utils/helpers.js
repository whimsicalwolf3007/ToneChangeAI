// Emotion color mapping
export const emotionColors = {
  happy: '#FFD700',
  sad: '#4169E1',
  angry: '#DC143C',
  fearful: '#9370DB',
  surprised: '#FF69B4',
  disgusted: '#32CD32',
  neutral: '#808080',
  sarcasm: '#FF8C00',
  excited: '#FF1493',
  frustrated: '#B22222'
};

// Tone descriptions
export const toneDescriptions = {
  polite: 'Courteous and respectful language',
  professional: 'Formal business communication',
  friendly: 'Warm and approachable tone',
  casual: 'Relaxed and informal style',
  formal: 'Very formal and precise language',
  enthusiastic: 'Excited and energetic tone',
  empathetic: 'Understanding and compassionate',
  confident: 'Assertive and self-assured',
  humble: 'Modest and respectful',
  urgent: 'Direct and time-sensitive'
};

// Format confidence percentage
export const formatConfidence = (confidence) => {
  return `${(confidence * 100).toFixed(1)}%`;
};

// Generate random client ID
export const generateClientId = () => {
  return Math.random().toString(36).substring(2, 11);
};

// Capitalize first letter
export const capitalizeFirst = (str) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};
