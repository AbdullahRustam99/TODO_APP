'use client';

import { createContext, useContext, useReducer, ReactNode, useEffect } from 'react';
import { Task, TaskFilters, TaskState, CreateTaskRequest, UpdateTaskRequest } from '@/lib/types';
import { apiClient } from '@/lib/api';
import { useAuth } from './AuthContext';

// Define action types
type TaskAction =
  | { type: 'SET_TASKS'; payload: Task[] }
  | { type: 'ADD_TASK'; payload: Task }
  | { type: 'UPDATE_TASK'; payload: Task }
  | { type: 'DELETE_TASK'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_FILTERS'; payload: TaskFilters }
  | { type: 'SET_CURRENT_VIEW'; payload: 'list' | 'grid' | 'calendar' }
  | { type: 'SET_COMPLETED'; payload: { id: string; completed: boolean } }
  | { type: 'SET_PRIORITY'; payload: { id: string; priority: 'low' | 'medium' | 'high' } };

// Initial state
const initialState: TaskState = {
  tasks: [],
  loading: false,
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
      return {
        ...state,
        tasks: action.payload,
        loading: false,
      };
    case 'ADD_TASK':
      return {
        ...state,
        tasks: [...state.tasks, action.payload],
      };
    case 'UPDATE_TASK':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id ? action.payload : task
        ),
      };
    case 'DELETE_TASK':
      return {
        ...state,
        tasks: state.tasks.filter(task => task.id !== action.payload),
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
      };
    case 'SET_FILTERS':
      return {
        ...state,
        filters: { ...state.filters, ...action.payload },
      };
    case 'SET_CURRENT_VIEW':
      return {
        ...state,
        currentView: action.payload,
      };
    case 'SET_COMPLETED':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id
            ? { ...task, completed: action.payload.completed }
            : task
        ),
      };
    case 'SET_PRIORITY':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id
            ? { ...task, priority: action.payload.priority }
            : task
        ),
      };
    default:
      return state;
  }
};

// Enhanced context type
interface TaskContextType extends TaskState {
  dispatch: React.Dispatch<TaskAction>;
  addTask: (task: Task) => void;
  updateTask: (task: Task) => void;
  deleteTask: (id: string) => void;
  setCompleted: (id: string, completed: boolean) => void;
  setPriority: (id: string, priority: 'low' | 'medium' | 'high') => void;
  setFilters: (filters: TaskFilters) => void;
  setCurrentView: (view: 'list' | 'grid' | 'calendar') => void;
  fetchTasks: () => Promise<void>;
  createTask: (taskData: CreateTaskRequest) => Promise<Task>;
  updateTaskAPI: (id: string, taskData: UpdateTaskRequest) => Promise<Task>;
  deleteTaskAPI: (id: string) => Promise<void>;
  toggleTaskCompletion: (id: string) => Promise<Task>;
  getTasksByStatus: (status: 'all' | 'active' | 'completed' | 'priority') => Task[];
  searchTasks: (query: string) => Task[];
}

// Create the context
const TaskContext = createContext<TaskContextType | undefined>(undefined);

// Provider component
export const TaskProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(taskReducer, initialState);
  const { token, user } = useAuth(); // Get the auth token and user from AuthContext

  const addTask = (task: Task) => {
    dispatch({ type: 'ADD_TASK', payload: task });
  };

  const updateTask = (task: Task) => {
    dispatch({ type: 'UPDATE_TASK', payload: task });
  };

  const deleteTask = (id: string) => {
    dispatch({ type: 'DELETE_TASK', payload: id });
  };

  const setCompleted = (id: string, completed: boolean) => {
    dispatch({ type: 'SET_COMPLETED', payload: { id, completed } });
  };

  const setPriority = (id: string, priority: 'low' | 'medium' | 'high') => {
    dispatch({ type: 'SET_PRIORITY', payload: { id, priority } });
  };

  const setFilters = (filters: TaskFilters) => {
    dispatch({ type: 'SET_FILTERS', payload: filters });
  };

  const setCurrentView = (view: 'list' | 'grid' | 'calendar') => {
    dispatch({ type: 'SET_CURRENT_VIEW', payload: view });
  };

  // API functions that connect to the backend
  const fetchTasks = async () => {
    // Prevent API call if user is not authenticated
    if (!user || !token) {
      dispatch({ type: 'SET_ERROR', payload: 'User not authenticated' });
      return;
    }

    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const userId = user?.id;
      if (!userId) {
        throw new Error('User ID is required to fetch tasks');
      }
      const response = await apiClient.get<Task[]>(`/api/${userId}/tasks`, token);
      dispatch({ type: 'SET_TASKS', payload: response });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error instanceof Error ? error.message : 'Failed to fetch tasks' });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const createTask = async (taskData: CreateTaskRequest): Promise<Task> => {
    // Prevent API call if user is not authenticated
    if (!user || !token) {
      throw new Error('User not authenticated');
    }

    try {
      const userId = user?.id;
      if (!userId) {
        throw new Error('User ID is required to create task');
      }
      const response = await apiClient.post<Task>(`/api/${userId}/tasks`, taskData, token);
      addTask(response);
      return response;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error instanceof Error ? error.message : 'Failed to create task' });
      throw error;
    }
  };

  const updateTaskAPI = async (id: string, taskData: UpdateTaskRequest): Promise<Task> => {
    // Prevent API call if user is not authenticated
    if (!user || !token) {
      throw new Error('User not authenticated');
    }

    try {
      const userId = user?.id;
      if (!userId) {
        throw new Error('User ID is required to update task');
      }
      const response = await apiClient.put<Task>(`/api/${userId}/tasks/${id}`, taskData, token);
      updateTask(response);
      return response;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error instanceof Error ? error.message : 'Failed to update task' });
      throw error;
    }
  };

  const deleteTaskAPI = async (id: string) => {
    // Prevent API call if user is not authenticated
    if (!user || !token) {
      throw new Error('User not authenticated');
    }

    try {
      const userId = user?.id;
      if (!userId) {
        throw new Error('User ID is required to delete task');
      }
      await apiClient.delete(`/api/${userId}/tasks/${id}`, token);
      deleteTask(id);
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error instanceof Error ? error.message : 'Failed to delete task' });
      throw error;
    }
  };

  const toggleTaskCompletion = async (id: string): Promise<Task> => {
    // Prevent API call if user is not authenticated
    if (!user || !token) {
      throw new Error('User not authenticated');
    }

    try {
      const userId = user?.id;
      if (!userId) {
        throw new Error('User ID is required to toggle task completion');
      }
      const task = state.tasks.find(t => t.id === id);
      if (!task) throw new Error('Task not found');

      const response = await apiClient.patch<Task>(`/api/${userId}/tasks/${id}/complete`, { completed: !task.completed }, token);
      updateTask(response);
      setCompleted(id, response.completed);
      return response;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error instanceof Error ? error.message : 'Failed to toggle task completion' });
      throw error;
    }
  };

  const getTasksByStatus = (status: 'all' | 'active' | 'completed' | 'priority'): Task[] => {
    switch (status) {
      case 'active':
        return state.tasks.filter(task => !task.completed);
      case 'completed':
        return state.tasks.filter(task => task.completed);
      case 'priority':
        return state.tasks.filter(task => task.priority === 'high');
      default:
        return state.tasks;
    }
  };

  const searchTasks = (query: string): Task[] => {
    if (!query) return state.tasks;
    return state.tasks.filter(task =>
      task.title.toLowerCase().includes(query.toLowerCase()) ||
      (task.description && task.description.toLowerCase().includes(query.toLowerCase()))
    );
  };

  // Fetch tasks when the context is initialized
  useEffect(() => {
    if (token && user) {
      fetchTasks();
    }
  }, [token, user]);

  const value = {
    ...state,
    dispatch,
    addTask,
    updateTask,
    deleteTask,
    setCompleted,
    setPriority,
    setFilters,
    setCurrentView,
    fetchTasks,
    createTask,
    updateTaskAPI,
    deleteTaskAPI,
    toggleTaskCompletion,
    getTasksByStatus,
    searchTasks,
  };

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
};

// Custom hook to use the TaskContext
export const useTaskContext = () => {
  const context = useContext(TaskContext);
  if (context === undefined) {
    throw new Error('useTaskContext must be used within a TaskProvider');
  }
  return context;
};