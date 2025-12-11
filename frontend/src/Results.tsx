import './Results.css'

interface Insights {
  top_loyal_cards: Array<{ name: string; count: number; icon: string }>
  longest_win_streak: number
  comeback_king_percentage: number
  deck_archetype: string
  rare_gem: { name: string; win_rate: number; usage: number }
  nemesis: { name: string; tag: string; wins: number; losses: number; total: number; message: string }
  peak_performance_hours: { hour: string; win_rate: number }
  trophy_roller_coaster: {
    current: number
    best: number
    biggest_gain: number
    biggest_loss: number
    total_swing: number
    recent_changes: number[]
  }
  player_name: string
  player_tag: string
}

interface ResultsProps {
  insights: Insights
  onTryAgain: () => void
}

function Results({ insights, onTryAgain }: ResultsProps) {
  return (
    <div className="results-app">
      <div className="results-container">
        {/* Header */}
        <header className="results-header">
          <div className="crown-icon">👑</div>
          <h1 className="results-title">Your Clash Royale Wrapped</h1>
          <p className="results-subtitle">{insights.player_name} {insights.player_tag}</p>
        </header>

        {/* Try Again Button */}
        <button className="try-again-button" onClick={onTryAgain}>
          🔄 Try Another Tag
        </button>

        {/* Insights Grid */}
        <div className="insights-grid">
          {/* Top 3 Loyal Cards */}
          <div className="insight-card">
            <div className="insight-icon">🎯</div>
            <h2 className="insight-title">Top 3 Loyal Cards</h2>
            <div className="loyal-cards">
              {insights.top_loyal_cards.map((card, index) => (
                <div key={index} className="loyal-card-item">
                  <div className="card-rank">#{index + 1}</div>
                  <div className="card-name">{card.name}</div>
                  <div className="card-count">{card.count} battles</div>
                </div>
              ))}
              {insights.top_loyal_cards.length === 0 && (
                <p className="no-data">No card data available</p>
              )}
            </div>
          </div>

          {/* Longest Win Streak */}
          <div className="insight-card">
            <div className="insight-icon">🔥</div>
            <h2 className="insight-title">Longest Win Streak</h2>
            <div className="streak-display">
              <span className="streak-number">{insights.longest_win_streak}</span>
              <span className="streak-label">consecutive wins</span>
            </div>
          </div>

          {/* Comeback King */}
          <div className="insight-card">
            <div className="insight-icon">⚡</div>
            <h2 className="insight-title">Comeback King</h2>
            <div className="percentage-display">
              <span className="percentage-number">{insights.comeback_king_percentage}%</span>
              <span className="percentage-label">of wins were comebacks</span>
            </div>
          </div>

          {/* Deck Archetype */}
          <div className="insight-card">
            <div className="insight-icon">🛡️</div>
            <h2 className="insight-title">Deck Archetype</h2>
            <div className="archetype-display">
              <span className="archetype-name">{insights.deck_archetype}</span>
            </div>
          </div>

          {/* Rare Gem */}
          <div className="insight-card">
            <div className="insight-icon">💎</div>
            <h2 className="insight-title">Rare Gem</h2>
            <div className="rare-gem-display">
              <div className="gem-name">{insights.rare_gem.name}</div>
              <div className="gem-stats">
                <span>{insights.rare_gem.win_rate}% win rate</span>
                <span>{insights.rare_gem.usage} uses</span>
              </div>
            </div>
          </div>

          {/* Nemesis */}
          <div className="insight-card">
            <div className="insight-icon">😤</div>
            <h2 className="insight-title">Nemesis</h2>
            <div className="nemesis-display">
              <div className="nemesis-name">{insights.nemesis.name}</div>
              <div className="nemesis-tag">{insights.nemesis.tag}</div>
              <div className="nemesis-stats">
                <span className="nemesis-wins">Wins: {insights.nemesis.wins}</span>
                <span className="nemesis-losses">Losses: {insights.nemesis.losses}</span>
              </div>
              {insights.nemesis.message && (
                <div className="nemesis-message">{insights.nemesis.message}</div>
              )}
            </div>
          </div>

          {/* Peak Performance Hours */}
          <div className="insight-card">
            <div className="insight-icon">⏰</div>
            <h2 className="insight-title">Peak Performance</h2>
            <div className="peak-hours-display">
              <span className="peak-hour">{insights.peak_performance_hours.hour}</span>
              <span className="peak-winrate">{insights.peak_performance_hours.win_rate}% win rate</span>
            </div>
          </div>

          {/* Trophy Roller Coaster */}
          <div className="insight-card trophy-card">
            <div className="insight-icon">🎢</div>
            <h2 className="insight-title">Trophy Roller Coaster</h2>
            <div className="trophy-stats">
              <div className="trophy-stat">
                <span className="stat-label">Current</span>
                <span className="stat-value">{insights.trophy_roller_coaster.current.toLocaleString()}</span>
              </div>
              <div className="trophy-stat">
                <span className="stat-label">Best</span>
                <span className="stat-value">{insights.trophy_roller_coaster.best.toLocaleString()}</span>
              </div>
              <div className="trophy-stat">
                <span className="stat-label">Biggest Gain</span>
                <span className="stat-value positive">+{insights.trophy_roller_coaster.biggest_gain}</span>
              </div>
              <div className="trophy-stat">
                <span className="stat-label">Biggest Loss</span>
                <span className="stat-value negative">{insights.trophy_roller_coaster.biggest_loss}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="results-footer">
          <p>Share your Clash Royale Wrapped!</p>
        </footer>
      </div>
    </div>
  )
}

export default Results

