import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Leaf, AlertCircle } from 'lucide-react';
import { authApi } from '../api';

export default function Login() {
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await authApi.login(phone, password);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Invalid credentials');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="mobile-app-container" style={{ justifyContent: 'center', backgroundColor: '#f0f7f4' }}>

            <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                <div style={{
                    display: 'inline-flex',
                    background: 'linear-gradient(135deg, var(--primary-light), var(--primary-dark))',
                    padding: '16px',
                    borderRadius: '50%',
                    marginBottom: '16px',
                    boxShadow: 'var(--shadow-md)'
                }}>
                    <Leaf color="white" size={40} />
                </div>
                <h1 style={{ color: 'var(--primary-dark)', fontSize: '2rem' }}>भारत-सेतु</h1>
                <p style={{ color: 'var(--text-muted)' }}>Farmer & VLE Partner App</p>
            </div>

            <div className="glass-card" style={{ margin: '0 20px' }}>
                <h2 style={{ marginBottom: '24px', textAlign: 'center' }}>Welcome Back</h2>

                {error && (
                    <div style={{
                        background: 'rgba(211, 47, 47, 0.1)',
                        color: 'var(--status-red)',
                        padding: '12px',
                        borderRadius: '8px',
                        marginBottom: '16px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        fontSize: '0.875rem'
                    }}>
                        <AlertCircle size={16} />
                        {error}
                    </div>
                )}

                <form onSubmit={handleLogin}>
                    <div className="input-group">
                        <label className="input-label">Phone Number</label>
                        <input
                            type="tel"
                            className="glass-input"
                            placeholder="e.g. 9000000003"
                            value={phone}
                            onChange={(e) => setPhone(e.target.value)}
                            required
                        />
                    </div>

                    <div className="input-group">
                        <label className="input-label">Password</label>
                        <input
                            type="password"
                            className="glass-input"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary"
                        style={{ width: '100%', marginTop: '8px' }}
                        disabled={loading}
                    >
                        {loading ? 'Authenticating...' : 'Sign In'}
                    </button>
                </form>

                <div style={{ textAlign: 'center', marginTop: '24px', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                    <p>Demo accounts:</p>
                    <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', marginTop: '8px' }}>
                        <span style={{ cursor: 'pointer', background: 'rgba(0,0,0,0.05)', padding: '2px 8px', borderRadius: '4px' }} onClick={() => { setPhone('9000000003'); setPassword('farmer123'); }}>Farmer</span>
                        <span style={{ cursor: 'pointer', background: 'rgba(0,0,0,0.05)', padding: '2px 8px', borderRadius: '4px' }} onClick={() => { setPhone('9000000002'); setPassword('vle123'); }}>VLE Partner</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
