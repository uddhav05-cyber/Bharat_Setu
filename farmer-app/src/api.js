import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Auth API
export const authApi = {
    login: async (phone, password) => {
        const response = await api.post('/auth/login', { phone, password });
        if (response.data.access_token) {
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('user', JSON.stringify({
                id: response.data.user_id,
                role: response.data.role,
                name: response.data.name
            }));
        }
        return response.data;
    },
    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
    },
    getUser: () => {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }
};

// Farm API
export const farmApi = {
    getFarms: async () => {
        const response = await api.get('/farms/');
        return response.data;
    }
};

// Voice API
export const voiceApi = {
    processVoice: async (text) => {
        // Standard mock format matching design.md VoiceLambda interface
        const response = await api.post('/voice/process', {
            transcribed_text: text,
            language: 'hi',
            timestamp: new Date().toISOString()
        });
        return response.data;
    }
};

// Certificate API
export const certApi = {
    getCertificates: async () => {
        const response = await api.get('/certificates/');
        return response.data;
    }
};

export default api;
