# ToneShift AI - Frontend

Modern React + Vite frontend for the ToneShift AI emotion-aware text rewriting application.

## Features

- 🎨 **Modern UI**: Clean, responsive design with smooth animations
- 📊 **Emotion Analysis**: Visualize detected emotions with color-coded badges and confidence bars
- ✍️ **Tone Rewriting**: Transform text into multiple tone styles with real-time preview
- 📋 **Copy to Clipboard**: Easily copy rewritten text
- 🎯 **10+ Tone Styles**: Professional, friendly, polite, casual, and more
- 📱 **Responsive**: Works seamlessly on desktop, tablet, and mobile

## Quick Start

### Prerequisites

- Node.js 18+ or npm/yarn/pnpm
- Backend API running on `http://localhost:8000`

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── EmotionAnalysis.jsx
│   │   ├── EmotionAnalysis.css
│   │   ├── ToneRewriter.jsx
│   │   └── ToneRewriter.css
│   ├── services/        # API services
│   │   └── api.js
│   ├── utils/           # Utility functions
│   │   └── helpers.js
│   ├── App.jsx          # Main App component
│   ├── App.css          # App styles
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies
└── vite.config.js       # Vite configuration
```

## API Configuration

The frontend connects to the backend API via proxy configuration in `vite.config.js`:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '')
  }
}
```

## Usage

1. **Enter your message** in the text area
2. **Click "Analyze Emotion"** to detect emotions with confidence scores
3. **Select a target tone** from the dropdown (polite, professional, friendly, etc.)
4. **Click "Rewrite Text"** to transform your message
5. **Copy the rewritten text** using the copy button

## Building for Production

```bash
npm run build
```

The build output will be in the `dist` directory. You can serve it with any static file server.

## Technologies Used

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **Lucide React** - Icon library
- **CSS3** - Styling with modern features

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

MIT
