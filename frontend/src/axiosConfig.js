import axios from 'axios';

const BASE_URL = '/api';

const getAPI = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true, // Habilita el envío y la recepción de cookies
});

const getAPImultipart = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'multipart/form-data',
    },
    withCredentials: true,
});



export { getAPI , getAPImultipart}
