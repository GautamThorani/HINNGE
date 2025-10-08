import axios from 'axios';
import type { UserLogin, UserRegistration, AuthResponse, TokenData } from '../types/auth';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`);
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => {
    console.log(`Success: ${response.status} - ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Error:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    });
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (credentials: UserLogin): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  register: async (userData: UserRegistration): Promise<any> => {
  try {
    const response = await api.post('/auth/register', userData);
    return response.data;
  } catch (error: any) {
    console.error('Registration API error:', error);
    throw error;
  }
 },
  validateToken: async (token: string): Promise<{ valid: boolean; user: TokenData }> => {
    const response = await api.get('/auth/validate', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },

  getCurrentUser: async (): Promise<any> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

export const mfaAPI = {
  setup: async (userId: string): Promise<any> => {
    const response = await api.post(`/mfa/setup/${userId}`);
    return response.data;
  },

  verify: async (userId: string, token: string): Promise<any> => {
    const response = await api.post('/mfa/verify', { 
      user_id: userId, 
      token: token 
    });
    return response.data;
  },

  getStatus: async (userId: string): Promise<any> => {
    const response = await api.get(`/mfa/status/${userId}`);
    return response.data;
  },

  enable: async (userId: string): Promise<any> => {
    const response = await api.post(`/mfa/enable/${userId}`);
    return response.data;
  },

  disable: async (userId: string): Promise<any> => {
    const response = await api.post(`/mfa/disable/${userId}`);
    return response.data;
  },
};

export const auditAPI = {
  getEvents: async (userId?: string, limit: number = 100): Promise<any> => {
    const url = userId ? `/audit/events/user/${userId}` : '/audit/events';
    const response = await api.get(url, { params: { limit } });
    return response.data;
  },

  getStats: async (): Promise<any> => {
    const response = await api.get('/audit/stats');
    return response.data;
  },
    getAuditLogs: async (userId?: string, limit: number = 100): Promise<any> => {
    const url = userId ? `/audit/events/user/${userId}` : '/audit/events';
    const response = await api.get(url, { params: { limit } });
    return response.data;
  },

  getAuditStats: async (): Promise<any> => {
    const response = await api.get('/audit/stats');
    return response.data;
  },

  queryAuditEvents: async (query: any): Promise<any> => {
    const response = await api.post('/audit/events/query', query);
    return response.data;
  },

  getEventTypes: async (): Promise<any> => {
    const response = await api.get('/audit/events/types');
    return response.data;
  },
};

export default api;