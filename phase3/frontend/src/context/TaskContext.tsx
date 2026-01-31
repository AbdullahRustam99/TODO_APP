'use client';

import { createContext, useContext, useReducer, ReactNode, useEffect, useCallback } from 'react';
import { Task, TaskFilters, TaskState, CreateTaskRequest, UpdateTaskRequest } from '@/lib/types';
import { apiClient } from '@/lib/api';
import { useAuth } from './AuthContext';
import { eventBus } from '@/lib/event-bus';
import { EventSourcePolyfill } from 'event-source-polyfill'; // Import the polyfill

// Define action types
type TaskAction =
  | { type: 'SET_TASKS'; payload: Task[] }
  | { type: 'ADD_TASK'; payload: Task }
  | { type: 'UPDATE_TASK'; payload: Task }
  | { type: 'DELETE_TASK'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_FILTERS'; payload: TaskFilters }
  | { type: 'SET_CURRENT_VIEW'; payload: 'list' | 'grid' | 'calendar' };

// Initial state
const initialState: TaskState = {
  tasks: [],
  loading: true, // Start with loading true
  error: null,
  filters: {
    status: 'all',
    priority: 'all',
    search: '',
  },
  currentView: 'list',
};

// Reducer function
const taskReducer = (state: TaskState, action: TaskAction): TaskState => {
  switch (action.type) {
    case 'SET_TASKS':
      return { ...state, tasks: action.payload, loading: false };
    case 'ADD_TASK':
      if (state.tasks.some(task => task.id === action.payload.id)) {
        return state;
      }
      return { ...state, tasks: [...state.tasks, action.payload] };
    case 'UPDATE_TASK':
      return { ...state, tasks: state.tasks.map(task => (task.id === action.payload.id ? action.payload : task)) };
    case 'DELETE_TASK':
      return { ...state, tasks: state.tasks.filter(task => task.id !== action.payload) };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'SET_FILTERS':
      return { ...state, filters: { ...state.filters, ...action.payload } };
    case 'SET_CURRENT_VIEW':
      return { ...state, currentView: action.payload };
    default:
      return state;
  }
};

// Context type
interface TaskContextType extends TaskState {
  fetchTasks: () => Promise<void>;
  createTask: (taskData: CreateTaskRequest) => Promise<void>;
  updateTask: (id: string, taskData: UpdateTaskRequest) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  toggleTaskCompletion: (id: string) => Promise<void>;
  setFilters: (filters: TaskFilters) => void;
  setCurrentView: (view: 'list' | 'grid' | 'calendar') => void;
  getTasksByStatus: (status: 'all' | 'active' | 'completed' | 'priority') => Task[];
  searchTasks: (query: string) => Task[];
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

// Provider component
export const TaskProvider = ({ children }: { children: React.ReactNode }) => {
  const [state, dispatch] = useReducer(taskReducer, initialState);
  const { token, user } = useAuth();

  const fetchTasks = useCallback(async () => {
    if (!user || !token) return;
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const tasks = await apiClient.get<Task[]>(`/api/${user.id}/tasks`, token);
      dispatch({ type: 'SET_TASKS', payload: tasks });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to fetch tasks';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      console.error(errorMessage);
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, [user, token]);

  const createTask = async (taskData: CreateTaskRequest) => {
    if (!user || !token) throw new Error('User not authenticated');
    const tempId = `temp-${Date.now()}`;
    const newTask: Task = {
      id: tempId,
      userId: user.id,
      ...taskData,
      completed: false, // Explicitly set completed for new tasks
      priority: taskData.priority ?? 'medium', // Explicitly set priority
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    dispatch({ type: 'ADD_TASK', payload: newTask });
    try {
      await apiClient.post(`/api/${user.id}/tasks`, taskData, token);
      await fetchTasks();
    } catch (error) {
      console.error('Failed to create task:', error);
      dispatch({ type: 'DELETE_TASK', payload: tempId });
      dispatch({ type: 'SET_ERROR', payload: 'Failed to save new task.' });
    }
  };

  const updateTask = async (id: string, taskData: UpdateTaskRequest) => {
    if (!user || !token) throw new Error('User not authenticated');
    const originalTask = state.tasks.find(t => t.id === id);
    if (!originalTask) {
      console.error(`Task with id ${id} not found for update.`);
      return;
    }
    const originalTasks = state.tasks;
    const updatedTask = { ...originalTask, ...taskData };
    dispatch({ type: 'UPDATE_TASK', payload: updatedTask as Task });
    try {
      await apiClient.put(`/api/${user.id}/tasks/${id}`, taskData, token);
    } catch (error) {
      console.error('Failed to update task:', error);
      dispatch({ type: 'SET_TASKS', payload: originalTasks });
      dispatch({ type: 'SET_ERROR', payload: 'Failed to update task.' });
    }
  };

  const deleteTask = async (id: string) => {
    if (!user || !token) throw new Error('User not authenticated');

    try {
      // Simply send the delete request. The SSE event will handle the UI refresh.
      await apiClient.delete(`/api/${user.id}/tasks/${id}`, token);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      console.error('Failed to delete task:', errorMessage, error);
      // Optionally, you can dispatch an error to the UI here
      dispatch({ type: 'SET_ERROR', payload: `Failed to delete task: ${errorMessage}` });
    }
  };

  const toggleTaskCompletion = async (id: string) => {
    const task = state.tasks.find(t => t.id === id);
    if (!task) return;
    await updateTask(id, { completed: !task.completed });
  };

  const setFilters = (filters: TaskFilters) => dispatch({ type: 'SET_FILTERS', payload: filters });
  const setCurrentView = (view: 'list' | 'grid' | 'calendar') => dispatch({ type: 'SET_CURRENT_VIEW', payload: view });

  const getTasksByStatus = (status: 'all' | 'active' | 'completed' | 'priority'): Task[] => {
    switch (status) {
      case 'active': return state.tasks.filter(task => !task.completed);
      case 'completed': return state.tasks.filter(task => task.completed);
            case 'priority':
              return state.tasks.filter(task => task.priority === 'high' || task.priority === 'medium');
      default: return state.tasks;
    }
  };

  const searchTasks = (query: string): Task[] => {
    if (!query) return state.tasks;
    return state.tasks.filter(task =>
      task.title.toLowerCase().includes(query.toLowerCase()) ||
      (task.description && task.description.toLowerCase().includes(query.toLowerCase()))
    );
  };

  useEffect(() => {
    if (token && user) {
      fetchTasks();
    }

    let eventSource: EventSourcePolyfill | null = null;
    if (user && token) {
      const backendBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:3001';
      const sseUrl = `${backendBaseUrl}/api/events`;

      eventSource = new EventSourcePolyfill(sseUrl, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      eventSource.onopen = () => console.log('SSE connection opened.');
      eventSource.onmessage = (event) => console.log('SSE message received:', event);
      eventSource.addEventListener('task_refresh', () => {
        console.log('SSE task_refresh event received, fetching tasks...');
        fetchTasks();
      });
      eventSource.onerror = (error) => {
        console.error('SSE Error:', error);
        eventSource?.close();
      };
    }

    return () => {
      if (eventSource) {
        console.log('Closing SSE connection.');
        eventSource.close();
      }
      eventBus.off('tasks-updated', fetchTasks);
    };
  }, [token, user, fetchTasks]);

  const value = { ...state, fetchTasks, createTask, updateTask, deleteTask, toggleTaskCompletion, setFilters, setCurrentView, getTasksByStatus, searchTasks };

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
};

export const useTaskContext = () => {
  const context = useContext(TaskContext);
  if (context === undefined) {
    throw new Error('useTaskContext must be used within a TaskProvider');
  }
  return context;
};