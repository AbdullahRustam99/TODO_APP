import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { getAuthToken, removeAuthToken } from './auth';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach auth token
apiClient.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = getAuthToken();
    if (token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`,
      };
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle 401 errors
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Clear stored auth token
      removeAuthToken();

      // Reset auth state by removing user data
      if (typeof window !== 'undefined') {
        localStorage.removeItem('user');
      }

      // Redirect to login page
      if (typeof window !== 'undefined') {
        // Use window.location for immediate redirect without Next.js router dependency
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;