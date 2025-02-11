import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface User {
  id: number;
  username: string;
  email: string;
  points: number;
}

export interface Comment {
  id: number;
  content: string;
  author_id: number;
  quiz_id: number;
  parent_id?: number;
  created_at: string;
  updated_at: string;
  likes_count: number;
  author_username: string;
}

export interface Quiz {
  id: number;
  title: string;
  description?: string;
  quiz_type: string;
  time_limit?: number;
  attempt_count: number;
  creator_id: number;
  answers?: Array<{
    correct_answer: string;
    aliases: string[];
    position: number;
  }>;
  comments?: Comment[];
}

export interface QuizAttempt {
  answers: string[];
  completion_time: number;
}

export const auth = {
  register: async (username: string, email: string, password: string) => {
    const response = await api.post('/api/register', { username, email, password });
    localStorage.setItem('token', response.data.access_token);
    return response.data;
  },

  login: async (email: string, password: string) => {
    const response = await api.post('/api/login', { email, password });
    localStorage.setItem('token', response.data.access_token);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
  },
};

export const quizzes = {
  list: async (page = 1, limit = 10, search?: string) => {
    const params = new URLSearchParams({
      skip: ((page - 1) * limit).toString(),
      limit: limit.toString(),
      ...(search && { search }),
    });
    const response = await api.get(`/api/quizzes?${params}`);
    return response.data;
  },

  get: async (id: number) => {
    const response = await api.get(`/api/quizzes/${id}`);
    return response.data;
  },

  create: async (quiz: Omit<Quiz, 'id' | 'creator_id' | 'attempt_count'>) => {
    const response = await api.post('/api/quizzes', quiz);
    return response.data;
  },

  submitAttempt: async (quizId: number, attempt: QuizAttempt) => {
    const response = await api.post(`/api/quizzes/${quizId}/attempts`, attempt);
    return response.data;
  },

  getComments: async (quizId: number) => {
    const response = await api.get(`/api/quizzes/${quizId}/comments`);
    return response.data;
  },

  addComment: async (quizId: number, content: string) => {
    const response = await api.post(`/api/quizzes/${quizId}/comments`, { content });
    return response.data;
  },
};

export const comments = {
  reply: async (commentId: number, content: string) => {
    const response = await api.post(`/api/comments/${commentId}/replies`, { content });
    return response.data;
  },

  update: async (commentId: number, content: string) => {
    const response = await api.put(`/api/comments/${commentId}`, { content });
    return response.data;
  },

  delete: async (commentId: number) => {
    const response = await api.delete(`/api/comments/${commentId}`);
    return response.data;
  },
};
