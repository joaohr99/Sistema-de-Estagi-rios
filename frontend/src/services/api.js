// frontend/src/services/api.js

import axios from 'axios';

// Instância do Axios para API Django
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
    headers:{
        'Content-Type': 'application/json',
    }
})

// Interceptor para adicionar o token JWT em todas as requisições autenticadas.

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('acess_token'); //Obtém o token do localStorage
        if (token) {
            config.headers.Authorization = 'Bearer ${token}';
    }
    return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;