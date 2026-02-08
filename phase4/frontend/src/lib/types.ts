// Type definitions for Todo App frontend

// User interface
export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  createdAt: string;
  updatedAt: string;
}

// Task interface with all properties
export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  dueDate?: string;
  createdAt: string;
  updatedAt: string;
  userId: string;
  tags?: string[];
  category?: string;
  estimatedTime?: number; // in minutes
  actualTime?: number; // in minutes
  subtasks?: Subtask[];
}

// Subtask interface for nested tasks
export interface Subtask {
  id: string;
  title: string;
  completed: boolean;
  taskId: string;
}

// Task filters interface
export interface TaskFilters {
  status?: 'all' | 'active' | 'completed';
  priority?: 'all' | 'low' | 'medium' | 'high';
  search?: string;
  category?: string;
  dueDate?: string;
  tags?: string[];
}

// Authentication state interface
export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

// Task state interface
export interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  filters: TaskFilters;
  currentView: 'list' | 'grid' | 'calendar';
}

// API response interface
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message: string;
  error?: string;
  statusCode: number;
}

// Form input types
export interface TaskFormInputs {
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high';
  dueDate?: string;
  category?: string;
  tags?: string[];
  estimatedTime?: number;
}

export interface LoginFormInputs {
  email: string;
  password: string;
}

export interface RegisterFormInputs {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

// Theme context type
export type Theme = 'light' | 'dark' | 'system';

// Notification types
export interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  timestamp: string;
  read: boolean;
}

// Priority levels with display properties
export interface PriorityLevel {
  level: 'low' | 'medium' | 'high';
  label: string;
  color: string;
  icon: string;
}

// Filter options
export interface FilterOption {
  id: string;
  label: string;
  value: string;
  count?: number;
}

// Dashboard statistics
export interface DashboardStats {
  totalTasks: number;
  completedTasks: number;
  pendingTasks: number;
  overdueTasks: number;
  highPriorityTasks: number;
  weeklyProgress: number;
}

// Authentication response types
export interface AuthResponse {
  user: User;
  token: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name?: string;
}

export interface LoginResponse {
  user: User;
  token: string;
}

export interface RegisterResponse {
  user: User;
  token: string;
}

// Task API request/response types
export interface CreateTaskRequest {
  title: string;
  description: string;
  completed?: boolean;
  priority?: 'high' | 'medium' | 'low';
  due_date?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'high' | 'medium' | 'low';
  due_date?: string;
}