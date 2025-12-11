# Clash Royale Wrapped 🎮👑

TRY IT HERE: https://clash-royale-wrapped2.vercel.app/

A Spotify Wrapped-style experience for Clash Royale! Enter your player tag and discover fascinating insights about your gameplay, including your most used cards, win streaks, deck archetype, and more.

## Features

- 🎯 **Top 3 Loyal Cards** - Your most frequently used cards
- 🔥 **Longest Win Streak** - Your best consecutive wins
- ⚡ **Comeback King** - Percentage of comeback victories
- 🛡️ **Deck Archetype** - Your playstyle classification
- 💎 **Rare Gem** - Rarely used card with high win rate
- 😤 **Nemesis** - Your most frequent opponent with win/loss record
- ⏰ **Peak Performance Hours** - Best time of day to play
- 🎢 **Trophy Roller Coaster** - Your trophy journey and biggest swings

## Tech Stack

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI + Python
- **API**: Clash Royale Official API

## Setup

### Prerequisites

- Node.js (v18+)
- Python (v3.9+)
- Clash Royale API Token ([Get one here](https://developer.clashroyale.com/))

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Add your Clash Royale API token to `.env`:
```
CLASH_ROYALE_API_TOKEN=your_api_token_here
```

5. Start the backend server:
```bash
uvicorn main:app --reload
```

The API will run at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run at `http://localhost:5173`

## Usage

1. Open the frontend in your browser
2. Enter your Clash Royale player tag (e.g., `#ABC123XY`)
3. Click "Generate My Wrapped"
4. View your personalized Clash Royale insights!

## Project Structure

```
clash-royale-wrapped/
├── backend/
│   ├── api/
│   │   ├── clash_royale.py    # Clash Royale API client
│   │   └── analysis.py         # Insight generation logic
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── main.py                 # FastAPI application
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx             # Main input page
│   │   ├── Results.tsx         # Results display page
│   │   └── ...
│   └── package.json            # Node dependencies
└── README.md
```

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

Quick deployment options:
- **Frontend**: Deploy to [Vercel](https://vercel.com) or [Netlify](https://netlify.com)
- **Backend**: Deploy to [Railway](https://railway.app) or [Render](https://render.com)

## Notes

- The Clash Royale API has rate limits (typically 300 requests per 60 seconds)
- Battle log data may be limited or unavailable for some players
- Make sure to keep your API token secure and never commit it to version control
- For production, update CORS settings in `backend/main.py` or via `ALLOWED_ORIGINS` environment variable

## License

MIT
