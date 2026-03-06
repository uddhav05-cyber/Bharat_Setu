import { useState } from 'react'
import './index.css'
import Dashboard from './pages/Dashboard'
import CrisisMap from './pages/CrisisMap'
import TrafficLight from './pages/TrafficLight'
import DataExport from './pages/DataExport'

const PAGES = {
  dashboard: { label: 'Dashboard', icon: '📊', component: Dashboard },
  crisis: { label: 'Crisis Map', icon: '🗺️', component: CrisisMap },
  traffic: { label: 'Traffic Light', icon: '🚦', component: TrafficLight },
  export: { label: 'Data Export', icon: '📥', component: DataExport },
}

function App() {
  const [activePage, setActivePage] = useState('dashboard')
  const PageComponent = PAGES[activePage].component

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <h1>भारत-सेतु</h1>
          <p>Admin Dashboard</p>
        </div>

        <nav className="sidebar-nav">
          {Object.entries(PAGES).map(([key, { label, icon }]) => (
            <button
              key={key}
              className={`nav-link ${activePage === key ? 'active' : ''}`}
              onClick={() => setActivePage(key)}
            >
              <span className="nav-icon">{icon}</span>
              {label}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div style={{ marginBottom: '4px', fontWeight: '600', color: 'var(--text-secondary)' }}>
            v1.0.0-pilot
          </div>
          <div>Carbon-Kosh • Gram-Twin • Migration-Shield</div>
        </div>
      </aside>

      {/* Main content */}
      <main className="main-content">
        <PageComponent />
      </main>
    </div>
  )
}

export default App
