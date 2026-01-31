// Custom hook for task management
import { useState, useEffect } from 'react';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '@/lib/types';
import { apiClient } from '@/lib/api';
import { useAuth } from '@/context/AuthContext';
import {AuthResponse} from '@/lib/auth';
export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { user, token } = useAuth() as AuthResponse

  // Fetch all tasks
  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      if (!user) {
        throw new Error('User not authenticated');
      }

      const response = await apiClient.get<Task[]>(`/api/${user.id}/tasks`, token);

      // The response should be an array of tasks
      setTasks(response);
    } catch (err) {
      setError((err as Error).message);
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  // Create a new task
  const createTask = async (taskData: CreateTaskRequest) => {
    try {
      setLoading(true);
      setError(null);

      if (!user) {
        throw new Error('User not authenticated');
      }

      // Ensure priority is set, default to 'medium' if not provided
      const taskDataWithDefaults = {
        ...taskData,
        priority: taskData.priority || 'medium'
      };

      // Call the backend API to create the task
      const response = await apiClient.post<Task>(`/api/${user.id}/tasks`, taskDataWithDefaults, token);
      const newTask = response;

      // Update the local state with the new task
      setTasks(prevTasks => [...prevTasks, newTask]);

      return newTask;
    } catch (err) {
      let errorMessage = 'Failed to create task';
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err && typeof err === 'object' && 'message' in err) {
        errorMessage = String((err as any).message);
      } else if (err) {
        errorMessage = String(err);
      }
      setError(errorMessage);
      console.error('Error creating task:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Update an existing task
  const updateTask = async (id: string, taskData: UpdateTaskRequest) => {
    try {
      setLoading(true);
      setError(null);

      if (!user) {
        throw new Error('User not authenticated');
      }

      // Ensure priority is handled properly
      const taskDataWithDefaults = {
        ...taskData,
        priority: taskData.priority
      };

      // Call the backend API to update the task
      const response = await apiClient.put<Task>(`/api/${user.id}/tasks/${id}`, taskDataWithDefaults, token);
      const updatedTask = response;

      // Update the local state with the updated task
      setTasks(prevTasks => prevTasks.map(task =>
        task.id === id ? updatedTask : task
      ));

      return updatedTask;
    } catch (err) {
      let errorMessage = 'Failed to update task';
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err && typeof err === 'object' && 'message' in err) {
        errorMessage = String((err as any).message);
      } else if (err) {
        errorMessage = String(err);
      }
      setError(errorMessage);
      console.error('Error updating task:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Delete a task
  const deleteTask = async (id: string) => {
    try {
      setLoading(true);
      setError(null);

      if (!user) {
        throw new Error('User not authenticated');
      }

      // Call the backend API to delete the task
      await apiClient.delete(`/api/${user.id}/tasks/${id}`, token);

      // Update the local state by filtering out the deleted task
      setTasks(prevTasks => prevTasks.filter(task => task.id !== id));
    } catch (err) {
      let errorMessage = 'Failed to delete task';
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err && typeof err === 'object' && 'message' in err) {
        errorMessage = String((err as any).message);
      } else if (err) {
        errorMessage = String(err);
      }
      setError(errorMessage);
      console.error('Error deleting task:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Toggle task completion status
  const toggleTaskCompletion = async (id: string) => {
    try {
      setLoading(true);
      setError(null);

      if (!user || user.id === null) {
        throw new Error('User not authenticated or user ID is missing');
      }

      // Find the current task to get its current completion status
      const currentTask = tasks.find(task => task.id === id);

      // If the task doesn't exist in local state, we can still try to update it
      // We'll optimistically update the local state and then sync with API response
      const currentCompletedStatus = currentTask ? currentTask.completed : false;

      // Optimistically update the local state
      if (currentTask) {
        const optimisticUpdatedTasks = tasks.map(task =>
          task.id === id ? { ...task, completed: !currentCompletedStatus } : task
        );
        setTasks(optimisticUpdatedTasks);
      }

      // Call the backend API to update the task completion status
      const response = await apiClient.patch<Task>(`/api/${user.id}/tasks/${id}/complete`, {
        completed: !currentCompletedStatus
      }, token);
      const updatedTask = response;

      // If the task wasn't in the local state, add it; otherwise update it
      setTasks(prevTasks => {
        if (!currentTask) {
          return [...prevTasks, updatedTask];
        } else {
          return prevTasks.map(task =>
            task.id === id ? updatedTask : task
          );
        }
      });

      return updatedTask;
    } catch (err) {
      let errorMessage = 'Failed to toggle task completion';
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err && typeof err === 'object' && 'message' in err) {
        errorMessage = String((err as any).message);
      } else if (err) {
        errorMessage = String(err);
      }
      setError(errorMessage);
      console.error('Error toggling task completion:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Helper function to sort tasks by priority
  const sortTasksByPriority = (taskList: Task[]) => {
    return [...taskList].sort((a, b) => {
      // Define priority order: high > medium > low
      const priorityOrder = {
        'high': 3,
        'medium': 2,
        'low': 1,
        undefined: 0,
      };

      // Sort by priority first
      const priorityDiff = (priorityOrder[b.priority] || 0) - (priorityOrder[a.priority] || 0);

      // If priorities are equal, sort by completion status (incomplete first)
      if (priorityDiff === 0) {
        return a.completed === b.completed ? 0 : a.completed ? 1 : -1;
      }

      return priorityDiff;
    });
  };

  // Filter tasks by completion status and sort by priority
  const getTasksByStatus = (status: 'all' | 'active' | 'completed' | 'priority') => {
    let filteredTasks: Task[];

    switch (status) {
      case 'active':
        filteredTasks = tasks.filter(task => !task.completed);
        break;
      case 'completed':
        filteredTasks = tasks.filter(task => task.completed);
        break;
      case 'priority':
        filteredTasks = tasks.filter(task => task.priority === 'high' || task.priority === 'medium');
        break;
      default:
        filteredTasks = tasks;
    }

    // Sort the filtered tasks by priority
    return sortTasksByPriority(filteredTasks);
  };

  // Search tasks by title or description and sort by priority
  const searchTasks = (query: string) => {
    if (!query) return sortTasksByPriority(tasks);

    const filteredTasks = tasks.filter(task =>
      task.title.toLowerCase().includes(query.toLowerCase()) ||
      (task.description && task.description.toLowerCase().includes(query.toLowerCase()))
    );

    return sortTasksByPriority(filteredTasks);
  };

  useEffect(() => {
    if (user && token) {
      fetchTasks();
    }
  }, [user, token]);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    getTasksByStatus,
    searchTasks,
  };
};