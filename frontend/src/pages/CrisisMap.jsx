import { useState, useEffect } from 'react'

const API = 'http://localhost:8000'

export default function CrisisMap() {
    const [crisisData, setCrisisData] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetch(`${API}/dashboard/crisis-map`)
            .then(r => r.json())
            .then(setCrisisData)
            .catch(() => setCrisisData(getMockCrisisData()))
            .finally(() => setLoading(false))
    }, [])

    if (loading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
                Loading crisis map data...
            </div>
        )
    }

    const data = crisisData || getMockCrisisData()
    const villages = data.villages || data || []

    // Calculate summary stats
    const critical = villages.filter(v => v.status === 'CRITICAL').length
    const warnings = villages.filter(v => v.status === 'WARNING').length
    const safe = villages.filter(v => v.status === 'SAFE').length

    return (
        <>
            <div className="page-header">
                <h2>Crisis Map</h2>
                <p>Village cluster health monitoring — Boolean threshold crisis detection</p>
            </div>

            {/* Summary Bar */}
            <div className="kpi-grid" style={{ marginBottom: '24px' }}>
                <div className="kpi-card">
                    <div className="kpi-icon">🟢</div>
                    <div className="kpi-value" style={{ color: 'var(--green)' }}>{safe}</div>
                    <div className="kpi-label">Safe Villages</div>
                </div>
                <div className="kpi-card">
                    <div className="kpi-icon">🟡</div>
                    <div className="kpi-value" style={{ color: 'var(--yellow)' }}>{warnings}</div>
                    <div className="kpi-label">Warning</div>
                </div>
                <div className="kpi-card">
                    <div className="kpi-icon">🔴</div>
                    <div className="kpi-value" style={{ color: 'var(--red)' }}>{critical}</div>
                    <div className="kpi-label">Critical</div>
                </div>
            </div>

            {/* Village Cards */}
            <div className="crisis-grid">
                {villages.map((village, i) => (
                    <VillageCard key={i} village={village} />
                ))}
            </div>
        </>
    )
}

function VillageCard({ village }) {
    const statusClass = village.status === 'CRITICAL' ? 'critical' :
        village.status === 'WARNING' ? 'warning' : 'safe'

    // Determine which vital signs are breached
    const vitals = village.vital_signs || village

    return (
        <div className={`village-card ${statusClass}`}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                <div>
                    <div className="village-name">{village.name || village.cluster_name}</div>
                    <div className="village-district">{village.district || 'Pune'}, {village.state || 'Maharashtra'}</div>
                </div>
                <span className={`status status-${statusClass}`}>
                    {village.status === 'CRITICAL' ? '🔴' : village.status === 'WARNING' ? '🟡' : '🟢'}{' '}
                    {village.status}
                </span>
            </div>

            {/* Vital Signs */}
            <div className="vitals-grid">
                <VitalSign
                    label="Rainfall"
                    value={`${vitals.rainfall_percentage?.toFixed(0) || vitals.rainfall || '--'}%`}
                    threshold={50}
                    actual={vitals.rainfall_percentage || vitals.rainfall || 100}
                    unit="%"
                />
                <VitalSign
                    label="Water Access"
                    value={`${vitals.water_access_percentage?.toFixed(0) || vitals.water_access || '--'}%`}
                    threshold={30}
                    actual={vitals.water_access_percentage || vitals.water_access || 100}
                    unit="%"
                    invertThreshold
                />
                <VitalSign
                    label="NDVI Decline"
                    value={`${vitals.avg_ndvi_decline?.toFixed(0) || vitals.ndvi_decline || '--'}%`}
                    threshold={30}
                    actual={vitals.avg_ndvi_decline || vitals.ndvi_decline || 0}
                    isHigherBad
                />
                <VitalSign
                    label="Debt Ratio"
                    value={`${vitals.debt_to_income_ratio?.toFixed(1) || vitals.debt_ratio || '--'}`}
                    threshold={2.0}
                    actual={vitals.debt_to_income_ratio || vitals.debt_ratio || 0}
                    isHigherBad
                />
            </div>

            {/* Active Crisis Alerts */}
            {village.breached_thresholds && village.breached_thresholds.length > 0 && (
                <div style={{ marginTop: '16px', paddingTop: '12px', borderTop: '1px solid var(--border)' }}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '8px', fontWeight: '600' }}>
                        ⚠ BREACHED THRESHOLDS
                    </div>
                    {village.breached_thresholds.map((t, i) => (
                        <div
                            key={i}
                            style={{
                                fontSize: '0.8rem',
                                color: 'var(--red)',
                                marginBottom: '4px',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '6px',
                            }}
                        >
                            <span>•</span> {t}
                        </div>
                    ))}
                </div>
            )}

            {/* Population stats */}
            <div style={{ marginTop: '14px', display: 'flex', gap: '16px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                <span>👥 {village.total_population?.toLocaleString() || '--'}</span>
                <span>🌾 {village.total_farmers || '--'} farmers</span>
                <span>🌿 {village.total_carbon_tons?.toFixed(1) || '--'}t CO₂</span>
            </div>
        </div>
    )
}

function VitalSign({ label, value, threshold, actual, isHigherBad }) {
    let cls = 'safe'
    if (isHigherBad) {
        if (actual > threshold) cls = 'danger'
        else if (actual > threshold * 0.7) cls = 'warning'
    } else {
        if (actual < threshold) cls = 'danger'
        else if (actual < threshold * 1.3) cls = 'warning'
    }

    return (
        <div className="vital-item">
            <span className="vital-label">{label}</span>
            <span className={`vital-value ${cls}`}>{value}</span>
        </div>
    )
}

function getMockCrisisData() {
    return {
        villages: [
            {
                name: 'Shivajinagar Cluster',
                district: 'Pune',
                state: 'Maharashtra',
                status: 'SAFE',
                total_population: 2500,
                total_farmers: 45,
                total_carbon_tons: 28.5,
                vital_signs: {
                    rainfall_percentage: 85,
                    water_access_percentage: 72,
                    avg_ndvi_decline: 5,
                    debt_to_income_ratio: 0.8,
                },
                breached_thresholds: [],
            },
            {
                name: 'Kothrud Cluster',
                district: 'Pune',
                state: 'Maharashtra',
                status: 'CRITICAL',
                total_population: 1800,
                total_farmers: 32,
                total_carbon_tons: 15.2,
                vital_signs: {
                    rainfall_percentage: 42,
                    water_access_percentage: 25,
                    avg_ndvi_decline: 35,
                    debt_to_income_ratio: 2.5,
                },
                breached_thresholds: [
                    'Rainfall < 50% (42%)',
                    'Water Access < 30% (25%)',
                    'NDVI Decline > 30% (35%)',
                    'Debt Ratio > 2.0 (2.5)',
                ],
            },
            {
                name: 'Hadapsar Cluster',
                district: 'Pune',
                state: 'Maharashtra',
                status: 'SAFE',
                total_population: 1500,
                total_farmers: 28,
                total_carbon_tons: 10.0,
                vital_signs: {
                    rainfall_percentage: 55,
                    water_access_percentage: 45,
                    avg_ndvi_decline: 15,
                    debt_to_income_ratio: 1.2,
                },
                breached_thresholds: [],
            },
        ],
    }
}
