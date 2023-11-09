import axios from 'axios';

const BASE_URL = '/api';

const getAPI = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true, // Habilita el envío y la recepción de cookies
});

export { getAPI }
