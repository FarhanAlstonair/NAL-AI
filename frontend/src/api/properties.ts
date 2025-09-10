import { apiClient } from './client';
import type { Property, SearchFilters, ApiResponse, PaginatedResponse } from '@/types';

export const propertiesApi = {
  getProperties: async (filters?: SearchFilters & { page?: number; page_size?: number }): Promise<PaginatedResponse<Property>> => {
    const response = await apiClient.get('/properties/', { params: filters });
    return response.data;
  },

  getProperty: async (id: string): Promise<ApiResponse<Property>> => {
    const response = await apiClient.get(`/properties/${id}/`);
    return response.data;
  },

  createProperty: async (data: Partial<Property>): Promise<ApiResponse<Property>> => {
    const response = await apiClient.post('/properties/create/', data);
    return response.data;
  },

  updateProperty: async (id: string, data: Partial<Property>): Promise<ApiResponse<Property>> => {
    const response = await apiClient.put(`/properties/${id}/update/`, data);
    return response.data;
  },

  uploadPropertyMedia: async (propertyId: string, data: FormData): Promise<ApiResponse<any>> => {
    const response = await apiClient.post(`/properties/${propertyId}/media/`, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  searchProperties: async (query: string, filters?: SearchFilters): Promise<PaginatedResponse<Property>> => {
    const response = await apiClient.get('/properties/', {
      params: { q: query, ...filters },
    });
    return response.data;
  },
};