import axios from 'axios';

const API_BASE_URL = 'http://localhost:8096';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatResponse {
  response: string;
  timestamp: number;
}

export interface HealthResponse {
  status: string;
  mode: string;
  timestamp: number;
}

export const sendMessage = async (message: string): Promise<ChatResponse> => {
  try {
    const response = await api.post<ChatResponse>('/api/chat', {
      message,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.code === 'ECONNABORTED') {
        throw new Error('Request timed out. The system is processing your query, please try again.');
      }
      if (error.response?.status === 500) {
        throw new Error('Server error. Please try again.');
      }
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
    }
    throw new Error('Failed to send message. Please check your connection.');
  }
};

export const checkHealth = async (): Promise<HealthResponse> => {
  try {
    const response = await api.get<HealthResponse>('/api/health');
    return response.data;
  } catch (error) {
    throw new Error('Unable to connect to the RAG system.');
  }
};

export default api;
