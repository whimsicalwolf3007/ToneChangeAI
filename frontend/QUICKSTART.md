# ToneShift AI Frontend - Quick Setup Guide

## Prerequisites
- Node.js 18+ or npm

## Install & Run (3 steps)

1. **Navigate to frontend folder:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the app:**
   ```bash
   npm run dev
   ```

4. **Open browser:**
   Go to `http://localhost:3000`

## Important

Make sure the backend API is running on `http://localhost:8000` before starting the frontend.

## Start Backend First

In the root project directory:
```bash
uv run python run.py
```

Then start the frontend in a separate terminal.

## Troubleshooting

**Port already in use?**
```bash
# Change the port in vite.config.js:
server: {
  port: 3001  // Change to any available port
}
```

**Backend not connecting?**
- Verify backend is running on port 8000
- Check `vite.config.js` proxy settings
- Ensure no firewall is blocking connections
