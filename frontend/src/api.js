import axios from "axios"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./constants"

const isAuthEndpoint = (url) =>
    url?.includes('/api/login/') ||
    url?.includes('/api/register/') ||
    url?.includes('/api/login/refresh/');

let isRefreshing = false;
let failedQueue = [];

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
})

api.interceptors.request.use(
    (config) => {
        if (!isAuthEndpoint(config.url)) {
            const token = localStorage.getItem(ACCESS_TOKEN);
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        }
        return config;
    },
    (error) => Promise.reject(error)
);

const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });
    failedQueue = [];
}

api.interceptors.response.use(
    response => response, async (error) => {
        const originalRequest = error.config;

        if (
            error.response?.status === 401 && !originalRequest._retry && !isAuthEndpoint(originalRequest.url)
        ) {
            if (isRefreshing) {
                return new Promise((resolve, reject) => {
                    failedQueue.push({ resolve, reject });
                }).then(token => {
                    originalRequest.headers.Authorization = `Bearer ${token}`;
                    return api(originalRequest);
                });
            }
            originalRequest._retry = true;
            isRefreshing = true;
            const refreshToken = localStorage.getItem(REFRESH_TOKEN);
            if (!refreshToken) {
                localStorage.clear();
                window.location.href = '/login';
                return Promise.reject(error);
            }

            try {
                const res = await axios.post(`${import.meta.env.VITE_API_URL}/api/login/refresh/`, { refresh: refreshToken});
                const { access } = res.data;
                localStorage.setItem(ACCESS_TOKEN, access);
                processQueue(null, access);
                originalRequest.headers.Authorization = `Bearer ${access}`;
                return api(originalRequest);
            } catch (refreshError) {
                processQueue(refreshError, null);
                localStorage.clear();
                window.location.href = '/login';
                return Promise.reject(refreshError);
            } finally {
                isRefreshing = false;
            }
        }
        return Promise.reject(error);
    }
);

export default api