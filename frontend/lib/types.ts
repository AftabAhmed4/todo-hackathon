/**
 * TypeScript type definitions for authentication and tasks.
 *
 * Defines interfaces for User, Task, AuthResponse, and API errors.
 */

export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  message: string;
}

export interface ApiError {
  detail: string;
}

export interface SignupRequest {
  email: string;
  password: string;
}

export interface SigninRequest {
  email: string;
  password: string;
}

// Task Types

export enum TaskStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
}

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  status?: TaskStatus;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: TaskStatus;
}

export interface TaskListResponse {
  items: Task[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// Chat Types

export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

export interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: number;
}

export interface ChatResponse {
  response: string;
  conversation_id: number;
  message_id: number;
  tool_calls?: Array<{
    tool: string;
    arguments: Record<string, any>;
    result: Record<string, any>;
  }>;
}
