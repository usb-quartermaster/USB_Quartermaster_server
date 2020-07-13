import axios from 'axios';

export const qm_server = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    timeout: 5000,
    auth: {
        username: 'quartermaster',
        password: 'ChangeThis'
    }
});

export const refresh_frequency_ms = 10000