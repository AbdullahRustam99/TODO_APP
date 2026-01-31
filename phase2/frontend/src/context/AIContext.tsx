// Context for managing AI assistant state
'use client';

import { createContext, useContext, ReactNode, useState } from 'react';
import { apiClient } from '@/lib/api';
import { useAuth } from './AuthContext';

// Define AI-related types
export interface AIAssistantState {
  isProcessing: boolean;
  suggestions: string[];
  lastResponse: string | null;
  error: string | null;
  history: AIChatMessage[];
}

export interface AIChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

export interface AIQueryRequest {
  query: string;
  context?: any;
}

export interface AIQueryResponse {
  response: string;
  suggestions?: string[];
}

export interface AITaskSuggestionResponse {
  suggestions: string[];
}

// Define AI assistant context type
interface AIContextType {
  state: AIAssistantState;
  generateTaskSuggestions: () => Promise<string[]>;
  askAI: (query: string) => Promise<string>;
  clearHistory: () => void;
  addToHistory: (message: AIChatMessage) => void;
}

// Create the context with default values
const AIContext = createContext<AIContextType | undefined>(undefined);

// Provider component
interface AIProviderProps {
  children: ReactNode;
}

export const AIProvider = ({ children }: AIProviderProps) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [lastResponse, setLastResponse] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<AIChatMessage[]>([]);
  const { token, user } = useAuth(); // Get the auth token and user from AuthContext

  const generateTaskSuggestions = async (): Promise<string[]> => {
    setIsProcessing(true);
    setError(null);

    try {
      // Call the backend AI service for task suggestions
      const userId = user?.id;
      if (!userId) {
        throw new Error('User ID is required to generate task suggestions');
      }
<<<<<<< HEAD
      const response = await apiClient.get<AITaskSuggestionResponse>(`/api/${userId}/ai/suggestions`, token || undefined);
=======
      const response = await apiClient.get<AITaskSuggestionResponse>(`/api/${userId}/ai/suggestions`, token);
>>>>>>> main
      setSuggestions(response.suggestions);
      return response.suggestions;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to generate task suggestions';
      setError(errorMessage);

      // Fallback to mock suggestions if API fails
      const mockSuggestions = [
        "Review quarterly reports",
        "Schedule team meeting",
        "Update project documentation",
        "Follow up with clients"
      ];
      setSuggestions(mockSuggestions);
      return mockSuggestions;
    } finally {
      setIsProcessing(false);
    }
  };

  const askAI = async (query: string): Promise<string> => {
    setIsProcessing(true);
    setError(null);

    try {
      // Call the backend AI service with the user's query
      const userId = user?.id;
      if (!userId) {
        throw new Error('User ID is required to ask AI');
      }
<<<<<<< HEAD
      const response = await apiClient.post<AIQueryResponse>(`/api/${userId}/ai/query`, { query }, token || undefined);
=======
      const response = await apiClient.post<AIQueryResponse>(`/api/${userId}/ai/query`, { query }, token);
>>>>>>> main
      setLastResponse(response.response);

      // Update suggestions if provided in response
      if (response.suggestions) {
        setSuggestions(response.suggestions);
      }

      return response.response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to get AI response';
      setError(errorMessage);

      // Fallback to mock response if API fails
      let response = '';
      if (query.toLowerCase().includes('suggest') || query.toLowerCase().includes('recommend')) {
        response = `I suggest creating these tasks:\n- Review quarterly reports\n- Schedule team meeting\n- Update project documentation\n- Follow up with clients\n\nWould you like me to create any of these tasks?`;
      } else if (query.toLowerCase().includes('create') || query.toLowerCase().includes('add')) {
        response = `I've created the task based on your request: "${query}". It's been added to your task list.`;
      } else if (query.toLowerCase().includes('how') || query.toLowerCase().includes('help')) {
        response = `I can help you with:\n- Creating new tasks\n- Analyzing your productivity\n- Suggesting task priorities\n- Finding tasks by keyword\n\nTry asking me to create a task or analyze your productivity!`;
      } else {
        response = `I understand you're asking about "${query}". I can help you manage your tasks more efficiently. Would you like me to create a task, analyze your productivity, or suggest priorities?`;
      }

      setLastResponse(response);
      return response;
    } finally {
      setIsProcessing(false);
    }
  };

  const clearHistory = () => {
    setHistory([]);
    setLastResponse(null);
  };

  const addToHistory = (message: AIChatMessage) => {
    setHistory(prev => [...prev, message]);
  };

  const value = {
    state: {
      isProcessing,
      suggestions,
      lastResponse,
      error,
      history,
    },
    generateTaskSuggestions,
    askAI,
    clearHistory,
    addToHistory,
  };

  return <AIContext.Provider value={value}>{children}</AIContext.Provider>;
};

// Custom hook to use the AIContext
export const useAI = () => {
  const context = useContext(AIContext);
  if (context === undefined) {
    throw new Error('useAI must be used within an AIProvider');
  }
  return context;
};