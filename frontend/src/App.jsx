import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [health, setHealth] = useState('Chargement...')
  const [theme, setTheme] = useState('light')

  // 1. Appel à l'API FastAPI
  useEffect(() => {
    fetch('http://localhost:8000/health')
      .then(res => res.json())
      .then(data => setHealth(data.status))
      .catch(() => setHealth('Erreur de connexion'))
  }, [])

  // 2. Gestion du thème clair/sombre
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  return (
    <div style={{ padding: '2rem', textAlign: 'center', marginTop: '10vh' }}>

      {/* Bouton pour tester le thème */}
      <button
        onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
        style={{ padding: '10px 20px', borderRadius: '8px', border: '1px solid var(--border)', cursor: 'pointer', marginBottom: '2rem' }}
      >
        Changer de thème (Mode {theme})
      </button>

      {/* Carte principale */}
      <div style={{
        backgroundColor: 'var(--surface)',
        border: '1px solid var(--border)',
        padding: '3rem',
        borderRadius: '24px',
        maxWidth: '600px',
        margin: '0 auto',
        boxShadow: '0 10px 30px rgba(0,0,0,0.05)'
      }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>Landy<span style={{ color: 'var(--accent-hover)' }}>.</span></h1>
        <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>Land the job. Practice the interview.</p>

        {/* Statut du Backend */}
        <div style={{ padding: '1rem', borderRadius: '12px', backgroundColor: health === 'ok' ? '#5F863322' : '#FF9F4522', border: `1px solid ${health === 'ok' ? 'var(--accent)' : '#FF9F45'}` }}>
          <p style={{ margin: 0, fontWeight: '600' }}>
            Statut du Backend : {health === 'ok' ? 'Connecté 🟢' : health}
          </p>
        </div>
      </div>
    </div>
  )
}

export default App