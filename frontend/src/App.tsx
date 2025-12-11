import { useState } from 'react'
import './App.css'
import Results from './Results'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

interface PlayerData {
  success: boolean
  data: {
    player: any
    insights: any
  }
}

function App() {
  const [playerTag, setPlayerTag] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [playerData, setPlayerData] = useState<PlayerData | null>(null)

  const handleTryAgain = () => {
    setPlayerData(null)
    setPlayerTag('')
    setError(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    
    if (!playerTag.trim()) {
      setError('Please enter your Clash Royale tag')
      return
    }
    
    // Ensure tag has # prefix
    let cleanTag = playerTag.trim().toUpperCase()
    if (!cleanTag.startsWith('#')) {
      cleanTag = `#${cleanTag}`
    }
    
    setIsLoading(true)
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/player`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tag: cleanTag }),
      })

      const data = await response.json()

      if (!response.ok) {
        // Error from backend
        throw new Error(data.detail || 'Failed to fetch player data')
      }

      // Success - store player data
      setPlayerData(data)
      
    } catch (err) {
      // Handle errors - reset to starting screen
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred'
      setError(errorMessage)
      setPlayerData(null)
      
      // Reset form after showing error
      setTimeout(() => {
        setError(null)
        setPlayerTag('')
      }, 5000)
    } finally {
      setIsLoading(false)
    }
  }

  // Show results page if we have player data
  if (playerData && playerData.success && playerData.data.insights) {
    return <Results insights={playerData.data.insights} onTryAgain={handleTryAgain} />
  }

  return (
    <div className="app">
      <div className="container">
        {/* Header Section */}
        <header className="header">
          <div className="crown-icon">👑</div>
          <h1 className="title">Clash Royale Wrapped</h1>
          <p className="subtitle">Discover Your Battle Stats & Playstyle</p>
        </header>

        {/* Hero Section with Images */}
        <div className="hero-section">
          <div className="card-images">
            <div className="floating-card card-1">⚔️</div>
            <div className="floating-card card-2">🛡️</div>
            <div className="floating-card card-3">🏰</div>
            <div className="floating-card card-4">⚡</div>
          </div>
        </div>

        {/* Description Section */}
        <div className="description-section">
          <h2>What's Your Clash Royale Story?</h2>
          <p>
            Just like Spotify Wrapped, but for Clash Royale! Enter your player tag and 
            discover fascinating insights about your gameplay:
          </p>
          <ul className="features-list">
            <li>🎯 Your most used cards and favorite deck</li>
            <li>📊 Win rate trends and battle statistics</li>
            <li>🏆 Trophy progression and achievements</li>
            <li>👥 Which of your friends is dominating you daily</li>
            <li>📈 Your playstyle analysis and patterns</li>
          </ul>
        </div>

        {/* Error Message */}
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            <p>{error}</p>
          </div>
        )}

        {/* Input Form Section */}
        <div className="form-section">
          <form onSubmit={handleSubmit} className="tag-form">
            <div className="input-group">
              <label htmlFor="playerTag" className="input-label">
                Enter Your Clash Royale Player Tag
              </label>
              <div className="input-wrapper">
                <span className="tag-prefix">#</span>
                <input
                  id="playerTag"
                  type="text"
                  value={playerTag}
                  onChange={(e) => {
                    setPlayerTag(e.target.value.toUpperCase())
                    setError(null)
                  }}
                  placeholder="YOURTAG"
                  className="tag-input"
                  disabled={isLoading}
                  maxLength={15}
                />
              </div>
              <p className="input-hint">
                Your tag is the code after your username (e.g., #ABC123)
              </p>
            </div>
            <button 
              type="submit" 
              className="submit-button"
              disabled={isLoading || !playerTag.trim()}
            >
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing Your Stats...
                </>
              ) : (
                <>
                  🚀 Generate My Wrapped
                </>
              )}
            </button>
          </form>
        </div>

        {/* Footer */}
        <footer className="footer">
          <p>Powered by Clash Royale API</p>
        </footer>
      </div>
    </div>
  )
}

export default App
