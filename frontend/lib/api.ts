/**
 * API client wrapper with automatic JWT token attachment.
 *
 * Provides functions for making authenticated API requests.
 */

import { AuthResponse, SignupRequest, SigninRequest, Task, TaskCreate, TaskUpdate, TaskListResponse, ChatRequest, ChatResponse, Conversation, ChatMessage } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Get stored JWT token from localStorage.
 */
export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('auth_token');
}

/**
 * Store JWT token in localStorage.
 */
export function setToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('auth_token', token);
}

/**
 * Remove JWT token from localStorage.
 */
export function removeToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('auth_token');
}

/**
 * Make an authenticated API request.
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  // Merge existing headers from options
  if (options.headers) {
    const existingHeaders = new Headers(options.headers);
    existingHeaders.forEach((value, key) => {
      headers[key] = value;
    });
  }

  // Add Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: 'include', // Include cookies for httpOnly cookie support
  });

  // Handle 401 Unauthorized (expired or invalid token)
  // Skip session expiration handling for auth endpoints (signin/signup)
  const isAuthEndpoint = endpoint.includes('/auth/signin') || endpoint.includes('/auth/signup');

  if (response.status === 401 && !isAuthEndpoint) {
    removeToken();
    if (typeof window !== 'undefined') {
      window.location.href = '/signin?error=session_expired';
    }
    throw new Error('Session expired. Please sign in again.');
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * API client object with authentication and task methods.
 */
export const api = {
  /**
   * Sign up a new user.
   */
  async signup(data: SignupRequest): Promise<AuthResponse> {
    return apiRequest<AuthResponse>('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Sign in an existing user.
   */
  async signin(data: SigninRequest): Promise<AuthResponse> {
    return apiRequest<AuthResponse>('/api/auth/signin', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Health check endpoint.
   */
  async healthCheck(): Promise<{ status: string }> {
    return apiRequest<{ status: string }>('/health');
  },

  // Task CRUD Methods

  /**
   * Create a new task for a user.
   */
  async createTask(userId: number, data: TaskCreate): Promise<Task> {
    return apiRequest<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Get all tasks for a user with pagination.
   */
  async getTasks(userId: number, page: number = 1, pageSize: number = 20): Promise<TaskListResponse> {
    return apiRequest<TaskListResponse>(`/api/${userId}/tasks?page=${page}&page_size=${pageSize}`);
  },

  /**
   * Get a single task by ID.
   */
  async getTask(userId: number, taskId: number): Promise<Task> {
    return apiRequest<Task>(`/api/${userId}/tasks/${taskId}`);
  },

  /**
   * Update an existing task.
   */
  async updateTask(userId: number, taskId: number, data: TaskUpdate): Promise<Task> {
    return apiRequest<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a task.
   */
  async deleteTask(userId: number, taskId: number): Promise<{ message: string; id: number }> {
    return apiRequest<{ message: string; id: number }>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  },

  // Chat Methods

  /**
   * Send a chat message to the AI assistant.
   */
  async sendChatMessage(data: ChatRequest): Promise<ChatResponse> {
    return apiRequest<ChatResponse>('/api/chat/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Get all conversations for the authenticated user.
   */
  async getConversations(): Promise<Conversation[]> {
    return apiRequest<Conversation[]>('/api/chat/conversations');
  },

  /**
   * Get all messages in a conversation.
   */
  async getConversationMessages(conversationId: number): Promise<ChatMessage[]> {
    return apiRequest<ChatMessage[]>(`/api/chat/conversations/${conversationId}/messages`);
  },
};
