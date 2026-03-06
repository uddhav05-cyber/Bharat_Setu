import { useState } from 'react'

export default function TrafficLight() {
    const [verifications] = useState(getMockVerifications())

    // Stats
    const green = verifications.filter(v => v.status === 'GREEN').length
    const yellow = verifications.filter(v => v.status === 'YELLOW').length
    const red = verifications.filter(v => v.status === 'RED').length

    return (
        <>
            <div className="page-header">
                <h2>Traffic Light Protocol</h2>
                <p>VLE fraud detection — comparing ground reports against satellite verification</p>
            </div>

            {/* Stats */}
            <div className="kpi-grid" style={{ marginBottom: '24px' }}>
                <div className="kpi-card">
                    <div className="kpi-icon">🟢</div>
                    <div className="kpi-value" style={{ color: 'var(--green)' }}>{green}</div>
                    <div className="kpi-label">Auto-Approved</div>
                    <div className="kpi-trend up">Variance &lt; 10%</div>
                </div>
                <div className="kpi-card">
                    <div className="kpi-icon">🟡</div>
                    <div className="kpi-value" style={{ color: 'var(--yellow)' }}>{yellow}</div>
                    <div className="kpi-label">Flagged for Call</div>
                    <div className="kpi-trend" style={{ color: 'var(--yellow)', background: 'var(--yellow-bg)' }}>Variance 10-30%</div>
                </div>
                <div className="kpi-card">
                    <div className="kpi-icon">🔴</div>
                    <div className="kpi-value" style={{ color: 'var(--red)' }}>{red}</div>
                    <div className="kpi-label">Account Frozen</div>
                    <div className="kpi-trend down">Variance &gt; 30%</div>
                </div>
            </div>

            {/* VLE Table */}
            <div className="card" style={{ marginBottom: '24px' }}>
                <div className="card-header">
                    <span className="card-title">👤 VLE Trust Scores</span>
                </div>
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>VLE Name</th>
                            <th>Trust Score</th>
                            <th>Verifications</th>
                            <th>Accuracy</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {getMockVLEs().map((vle, i) => (
                            <tr key={i}>
                                <td style={{ fontWeight: '600' }}>{vle.name}</td>
                                <td>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                        <span className="trust-score" style={{
                                            fontSize: '1rem',
                                            fontWeight: '800',
                                            color: vle.trust > 70 ? 'var(--green)' :
                                                vle.trust > 40 ? 'var(--yellow)' : 'var(--red)',
                                        }}>
                                            {vle.trust}
                                        </span>
                                        <div className="progress-bar" style={{ width: '80px' }}>
                                            <div
                                                className={`progress-fill ${vle.trust > 70 ? 'green' : vle.trust > 40 ? 'yellow' : 'red'}`}
                                                style={{ width: `${vle.trust}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                </td>
                                <td>{vle.total}</td>
                                <td>{vle.accuracy}%</td>
                                <td>
                                    <span className={`status ${vle.accountStatus === 'ACTIVE' ? 'status-green' : 'status-red'}`}>
                                        {vle.accountStatus}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Recent Verifications */}
            <div className="card">
                <div className="card-header">
                    <span className="card-title">🔬 Verification History</span>
                </div>
                <div className="traffic-light-container">
                    {verifications.map((v, i) => (
                        <div key={i} className="tl-row">
                            <div className={`tl-light ${v.status.toLowerCase()}`}>
                                {v.status === 'GREEN' ? '✓' : v.status === 'YELLOW' ? '?' : '✕'}
                            </div>
                            <div className="tl-details">
                                <div className="tl-name">{v.farmer} — {v.crop}</div>
                                <div className="tl-meta">
                                    Variance: {v.variance}% • Confidence: {v.confidence}% • {v.source}
                                </div>
                                <div className="tl-meta" style={{ fontStyle: 'italic', marginTop: '2px' }}>
                                    {v.reasoning}
                                </div>
                            </div>
                            <div className="tl-trust">
                                <div className="trust-score" style={{
                                    color: v.trustDelta > 0 ? 'var(--green)' :
                                        v.trustDelta < 0 ? 'var(--red)' : 'var(--text-muted)',
                                }}>
                                    {v.trustDelta > 0 ? '+' : ''}{v.trustDelta}
                                </div>
                                <div className="trust-label">Trust Δ</div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </>
    )
}

function getMockVLEs() {
    return [
        { name: 'Ramesh Kumar', trust: 75, total: 24, accuracy: 88, accountStatus: 'ACTIVE' },
        { name: 'Priya Sharma', trust: 92, total: 45, accuracy: 96, accountStatus: 'ACTIVE' },
        { name: 'Raj Patel', trust: 35, total: 12, accuracy: 50, accountStatus: 'SUSPENDED' },
        { name: 'Anita Desai', trust: 68, total: 18, accuracy: 78, accountStatus: 'ACTIVE' },
    ]
}

function getMockVerifications() {
    return [
        {
            farmer: 'Suresh Patil',
            crop: 'Rice, 1.5 acres',
            status: 'GREEN',
            variance: 4.2,
            confidence: 92,
            source: 'Sentinel-2 Optical',
            reasoning: 'VLE data matches satellite verification. Auto-approved.',
            trustDelta: 2,
        },
        {
            farmer: 'Lakshmi Devi',
            crop: 'Wheat, 2.0 acres',
            status: 'YELLOW',
            variance: 18.5,
            confidence: 85,
            source: 'Sentinel-1 SAR',
            reasoning: 'Moderate variance detected. Flagged for verification call.',
            trustDelta: 0,
        },
        {
            farmer: 'Arun Jadhav',
            crop: 'Cotton, 3.0 acres',
            status: 'GREEN',
            variance: 7.1,
            confidence: 94,
            source: 'Sentinel-2 Optical',
            reasoning: 'VLE data matches satellite verification. Auto-approved.',
            trustDelta: 2,
        },
        {
            farmer: 'Meena Patil',
            crop: 'Sugarcane, 1.2 acres',
            status: 'RED',
            variance: 45.8,
            confidence: 91,
            source: 'Sentinel-1 SAR',
            reasoning: 'High variance detected. VLE account frozen for audit.',
            trustDelta: -15,
        },
        {
            farmer: 'Ganesh More',
            crop: 'Rice, 2.5 acres',
            status: 'GREEN',
            variance: 3.8,
            confidence: 88,
            source: 'Sentinel-2 Optical',
            reasoning: 'VLE data matches satellite verification. Auto-approved.',
            trustDelta: 2,
        },
        {
            farmer: 'Vijay Kulkarni',
            crop: 'Wheat, 1.8 acres',
            status: 'YELLOW',
            variance: 22.3,
            confidence: 75,
            source: 'Sentinel-1 SAR',
            reasoning: 'Satellite data uncertain. Manual review needed.',
            trustDelta: 0,
        },
    ]
}
