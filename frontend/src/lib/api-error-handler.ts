// Global error handler for API errors
import { removeAuthToken } from './auth';

// Handle 401 Unauthorized errors globally
export const handleUnauthorizedError = () => {
  // Clear stored auth token
  removeAuthToken();

  // Reset auth state by removing user data
  if (typeof window !== 'undefined') {
    localStorage.removeItem('user');
  }

  // Redirect to login page
  if (typeof window !== 'undefined') {
    window.location.href = '/login';
  }
};

// Check if response is a 401 error
export const isUnauthorizedError = (error: any): boolean => {
  if (error && typeof error === 'object') {
    if (error.status === 401 || (error.response && error.response.status === 401)) {
      return true;
    }
  }
  return false;
};

// Generic error handler that can be used in components
export const handleApiError = (error: any, onUnauthorized?: () => void) => {
  if (isUnauthorizedError(error)) {
    handleUnauthorizedError();
    if (onUnauthorized) {
      onUnauthorized();
    }
    return;
  }

  console.error('API Error:', error);
  throw error;
};