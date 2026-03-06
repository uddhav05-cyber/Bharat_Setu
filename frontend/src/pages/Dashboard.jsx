import { useState, useEffect } from 'react'

const API = 'http://localhost:8000'

export default function Dashboard() {
    const [metrics, setMetrics] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetch(`${API}/dashboard/metrics`)
            .then(r => r.json())
            .then(setMetrics)
            .catch(() => setMetrics(getMockMetrics()))
            .finally(() => setLoading(false))
    }, [])

    if (loading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
                Loading dashboard metrics...
            </div>
        )
    }

    const data = metrics || getMockMetrics()

    return (
        <>
            <div className="page-header">
                <h2>Dashboard Overview</h2>
                <p>Real-time metrics for Carbon-Kosh, Gram-Twin & Migration-Shield</p>
            </div>

            {/* KPI Cards */}
            <div className="kpi-grid">
                <KPICard
                    icon="🌾"
                    value={data.total_farmers}
                    label="Active Farmers"
                    trend="+12 this month"
                    trendDir="up"
                />
                <KPICard
                    icon="👤"
                    value={data.total_vles}
                    label="Active VLEs"
                    trend="All operational"
                    trendDir="up"
                />
                <KPICard
                    icon="🌿"
                    value={`${data.total_carbon_tons?.toFixed(1) || 0}t`}
                    label="Carbon Credits (CO₂)"
                    trend="+3.2t this quarter"
                    trendDir="up"
                />
                <KPICard
                    icon="🚨"
                    value={data.critical_villages}
                    label="Critical Villages"
                    trend={data.critical_villages > 0 ? 'Action needed' : 'All clear'}
                    trendDir={data.critical_villages > 0 ? 'down' : 'up'}
                />
                <KPICard
                    icon="✅"
                    value={data.total_verifications}
                    label="Verifications Run"
                    trend="+5 this week"
                    trendDir="up"
                />
                <KPICard
                    icon="💰"
                    value={`₹${((data.total_carbon_tons || 0) * 500).toLocaleString()}`}
                    label="Service Payments"
                    trend="e-RUPI + PFMS"
                    trendDir="up"
                />
            </div>

            {/* Bottom Section */}
            <div className="content-grid-2">
                {/* Recent Verifications */}
                <div className="card">
                    <div className="card-header">
                        <span className="card-title">🔬 Recent Verifications</span>
                    </div>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Farm</th>
                                <th>Status</th>
                                <th>Carbon</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(data.recent_verifications || getMockVerifications()).map((v, i) => (
                                <tr key={i}>
                                    <td style={{ fontWeight: '600' }}>{v.farm}</td>
                                    <td>
                                        <span className={`status status-${v.status.toLowerCase()}`}>
                                            {v.status === 'GREEN' ? '🟢' : v.status === 'YELLOW' ? '🟡' : '🔴'} {v.status}
                                        </span>
                                    </td>
                                    <td>{v.carbon}t</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* Module Status */}
                <div className="card">
                    <div className="card-header">
                        <span className="card-title">📡 Module Status</span>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        <ModuleStatus
                            name="Carbon-Kosh"
                            desc="Satellite Verification Engine"
                            pct={70}
                            color="green"
                        />
                        <ModuleStatus
                            name="Gram-Twin"
                            desc="Digital Twin Visualization"
                            pct={100}
                            color="green"
                        />
                        <ModuleStatus
                            name="Migration-Shield"
                            desc="Boolean Threshold Detection"
                            pct={100}
                            color="green"
                        />
                        <ModuleStatus
                            name="Payment Rails"
                            desc="e-RUPI + PFMS Mock Adapters"
                            pct={100}
                            color="yellow"
                        />
                    </div>
                </div>
            </div>
        </>
    )
}

function KPICard({ icon, value, label, trend, trendDir }) {
    return (
        <div className="kpi-card">
            <div className="kpi-icon">{icon}</div>
            <div className="kpi-value">{value}</div>
            <div className="kpi-label">{label}</div>
            <div className={`kpi-trend ${trendDir}`}>
                {trendDir === 'up' ? '↑' : '↓'} {trend}
            </div>
        </div>
    )
}

function ModuleStatus({ name, desc, pct, color }) {
    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <div style={{ fontWeight: '600', fontSize: '0.9rem' }}>{name}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{desc}</div>
                </div>
                <span className={`status status-${color === 'yellow' ? 'warning' : 'safe'}`}>
                    {pct === 100 ? 'Active' : `${pct}% Core`}
                </span>
            </div>
            <div className="progress-bar">
                <div className={`progress-fill ${color}`} style={{ width: `${pct}%` }}></div>
            </div>
        </div>
    )
}

function getMockMetrics() {
    return {
        total_farmers: 105,
        total_vles: 7,
        total_carbon_tons: 53.7,
        critical_villages: 1,
        total_verifications: 38,
        recent_verifications: getMockVerifications(),
    }
}

function getMockVerifications() {
    return [
        { farm: 'Rice Plot #001', status: 'GREEN', carbon: '1.2' },
        { farm: 'Wheat Plot #002', status: 'YELLOW', carbon: '0.8' },
        { farm: 'Cotton Plot #003', status: 'GREEN', carbon: '2.1' },
        { farm: 'Sugarcane #004', status: 'RED', carbon: '0.0' },
        { farm: 'Rice Plot #005', status: 'GREEN', carbon: '1.5' },
    ]
}
