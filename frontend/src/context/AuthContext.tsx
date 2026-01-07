// Context for managing authentication state
'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User } from '@/lib/types';
import { getAuthToken, removeAuthToken, setAuthToken, login as apiLogin, register as apiRegister, logout as apiLogout } from '@/lib/auth';
import { validateStoredToken, removeExpiredToken } from '@/lib/token-validator';

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (userData: User, token: string) => void;
  logout: () => void;
  register: (userData: User, token: string) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing token and user on initial load
    const storedToken = getAuthToken();

    if (storedToken) {
      // Validate the stored token before using it
      if (validateStoredToken()) {
        setToken(storedToken);
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
          try {
            setUser(JSON.parse(storedUser));
          } catch (error) {
            console.error('Error parsing stored user:', error);
          }
        }
      } else {
        // Token is expired, remove it
        removeAuthToken();
        localStorage.removeItem('user');
        console.log('Expired token removed');
      }
    }
    setLoading(false);
  }, []);

  const login = (userData: User, authToken: string) => {
    setUser(userData);
    setToken(authToken);
    setAuthToken(authToken);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const register = (userData: User, authToken: string) => {
    setUser(userData);
    setToken(authToken);
    setAuthToken(authToken);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const logout = async () => {
    if (token) {
      try {
        await apiLogout(token);
      } catch (error) {
        console.error('Error during logout:', error);
      }
    }
    setUser(null);
    setToken(null);
    removeAuthToken();
    localStorage.removeItem('user');
  };

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    register,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};