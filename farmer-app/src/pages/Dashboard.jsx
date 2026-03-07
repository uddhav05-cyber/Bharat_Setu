import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut, MapPin, Award, ShieldAlert, Mic, Menu } from 'lucide-react';
import { authApi, farmApi, certApi, voiceApi } from '../api';

export default function Dashboard() {
    const [user, setUser] = useState(null);
    const [farms, setFarms] = useState([]);
    const [certs, setCerts] = useState([]);
    const [isRecording, setIsRecording] = useState(false);
    const [voiceInput, setVoiceInput] = useState('');
    const [voiceResult, setVoiceResult] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const currentUser = authApi.getUser();
        if (!currentUser) {
            navigate('/login');
            return;
        }
        setUser(currentUser);
        loadData();
    }, [navigate]);

    const loadData = async () => {
        try {
            const farmsData = await farmApi.getFarms();
            setFarms(farmsData);
            const certsData = await certApi.getCertificates();
            setCerts(certsData);
        } catch (err) {
            console.error("Failed to load data", err);
        }
    };

    const handleLogout = () => {
        authApi.logout();
        navigate('/login');
    };

    const handleVoiceStart = () => {
        setIsRecording(true);
        setVoiceResult(null);
        // Simulate speech recognition
        setTimeout(() => setVoiceInput('verification requests for my cotton plot'), 1500);
    };

    const handleVoiceEnd = async () => {
        if (!isRecording) return;
        setIsRecording(false);

        if (voiceInput) {
            try {
                const result = await voiceApi.processVoice(voiceInput);
                setVoiceResult(result);
                setVoiceInput('');
            } catch (err) {
                console.error("Voice processing failed", err);
            }
        }
    };

    if (!user) return null;

    return (
        <div className="mobile-app-container">
            {/* App Header */}
            <header className="app-header flex-between">
                <div>
                    <h2 style={{ color: 'white', fontSize: '1.25rem' }}>भारत-सेतु</h2>
                    <p style={{ fontSize: '0.875rem', opacity: 0.9 }}>Welcome, {user.name}</p>
                </div>
                <button onClick={handleLogout} style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer' }}>
                    <LogOut size={24} />
                </button>
            </header>

            {/* Main Content Area */}
            <main className="app-content">

                {/* VLE Specific Trust Score Card */}
                {user.role === 'VLE' && (
                    <div className="glass-card mb-4" style={{
                        background: 'linear-gradient(135deg, rgba(46, 125, 50, 0.1), rgba(46, 125, 50, 0.05))',
                        borderLeft: '4px solid var(--primary)'
                    }}>
                        <div className="flex-between mb-4">
                            <h3 style={{ fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <ShieldAlert size={20} color="var(--primary)" />
                                Traffic Light Protocol
                            </h3>
                            <span className="status-badge status-green">🟢 GREEN</span>
                        </div>
                        <div className="flex-between">
                            <div>
                                <p className="input-label">Trust Score</p>
                                <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary-dark)' }}>92.5%</p>
                            </div>
                            <div style={{ textAlign: 'right' }}>
                                <p className="input-label">Variance</p>
                                <p style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>4.2%</p>
                            </div>
                        </div>
                    </div>
                )}

                {/* Section: My Farms */}
                <h3 className="mb-4" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <MapPin size={20} /> Registered Plots
                </h3>

                {farms.length === 0 ? (
                    <div className="glass-card text-center text-muted mb-4">
                        <p>No farms registered yet.</p>
                    </div>
                ) : (
                    farms.map((farm) => (
                        <div key={farm.id} className="glass-card mb-4">
                            <div className="flex-between mb-4">
                                <span style={{ fontWeight: 600 }}>{farm.crop_type.toUpperCase()}</span>
                                <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>{farm.size_acres} Acres</span>
                            </div>
                            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '16px' }}>
                                {farm.village}, {farm.district}
                            </p>
                            <div className="flex-between">
                                <span className="status-badge status-yellow">Verification Pending</span>
                                <button className="btn-outline" style={{ padding: '6px 12px', borderRadius: '4px', fontSize: '0.875rem', border: '1px solid var(--primary)', background: 'transparent' }}>
                                    Start Verification
                                </button>
                            </div>
                        </div>
                    ))
                )}

                {/* Voice Processing Result Modal overlay simulation */}
                {voiceResult && (
                    <div className="glass-card mb-4" style={{ borderLeft: '4px solid var(--accent)' }}>
                        <p className="input-label">Voice Command Parsed</p>
                        <p style={{ fontWeight: 600, marginBottom: '8px' }}>Intent: {voiceResult.intent}</p>
                        <pre style={{
                            background: 'rgba(0,0,0,0.05)',
                            padding: '8px',
                            borderRadius: '4px',
                            fontSize: '0.8rem',
                            overflowX: 'auto'
                        }}>
                            {JSON.stringify(voiceResult.entities, null, 2)}
                        </pre>
                        <button className="btn-accent" style={{ padding: '6px 12px', marginTop: '12px', width: '100%', borderRadius: '4px' }} onClick={() => setVoiceResult(null)}>
                            Dismiss
                        </button>
                    </div>
                )}

            </main>

            {/* Floating Push-to-Talk Button */}
            <button
                className={`voice-fab ${isRecording ? 'recording' : ''}`}
                onPointerDown={handleVoiceStart}
                onPointerUp={handleVoiceEnd}
                onPointerLeave={handleVoiceEnd}
                title="Press and hold to speak"
            >
                <Mic size={32} />
            </button>

            {/* Recording Indicator Text */}
            {isRecording && (
                <div style={{ position: 'fixed', bottom: '110px', width: '100%', textAlign: 'center', zIndex: 40, padding: '0 20px' }}>
                    <div className="glass-card" style={{ display: 'inline-block', padding: '12px 24px', borderRadius: 'var(--radius-full)' }}>
                        <p style={{ margin: 0, fontWeight: 600, color: 'var(--accent)' }}>
                            {voiceInput ? voiceInput : 'Listening...'}
                        </p>
                        <div className="waveform-bars">
                            <div className="bar"></div>
                            <div className="bar"></div>
                            <div className="bar"></div>
                            <div className="bar"></div>
                            <div className="bar"></div>
                        </div>
                    </div>
                </div>
            )}

        </div>
    );
}
