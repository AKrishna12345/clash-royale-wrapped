import { useState } from 'react'
import './App.css'

function App() {
  const [playerTag, setPlayerTag] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!playerTag.trim()) {
      alert('Please enter your Clash Royale tag')
      return
    }
    
    // Remove # if user included it
    const cleanTag = playerTag.replace(/^#/, '')
    
    setIsLoading(true)
    // TODO: Call backend API
    console.log('Submitting tag:', cleanTag)
    
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false)
      // Handle response here
    }, 2000)
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
                  onChange={(e) => setPlayerTag(e.target.value)}
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
