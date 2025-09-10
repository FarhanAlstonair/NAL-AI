import { apiClient } from './client';
import type { LoginCredentials, RegisterData, User, AuthTokens, ApiResponse } from '@/types';

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<ApiResponse<{ access: string; refresh: string; user: User }>> => {
    const response = await apiClient.post('/auth/login/', credentials);
    return response.data;
  },

  register: async (data: RegisterData): Promise<ApiResponse<{ user: User }>> => {
    const response = await apiClient.post('/auth/register/', data);
    return response.data;
  },

  refreshToken: async (refreshToken: string): Promise<ApiResponse<AuthTokens>> => {
    const response = await apiClient.post('/auth/refresh/', { refresh: refreshToken });
    return response.data;
  },

  logout: async (refreshToken?: string): Promise<ApiResponse<{ message: string }>> => {
    const response = await apiClient.post('/auth/logout/', { refresh: refreshToken });
    return response.data;
  },

  getProfile: async (): Promise<ApiResponse<User>> => {
    const response = await apiClient.get('/users/profile/');
    return response.data;
  },

  updateProfile: async (data: Partial<User>): Promise<ApiResponse<User>> => {
    const response = await apiClient.put('/users/profile/update/', data);
    return response.data;
  },
};