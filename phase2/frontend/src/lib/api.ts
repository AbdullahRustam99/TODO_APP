// API utilities and configuration
import { handleUnauthorizedError } from './api-error-handler';
import { refreshAuthToken, getAuthToken } from './auth';

// Get the base URL for API requests
export function getBaseURL(): string {
  // Use environment variable or default to localhost backend
  return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
}

// Default headers for API requests
export const defaultHeaders: HeadersInit = {
  'Content-Type': 'application/json',
};

// Function to get auth headers with JWT token
export function getAuthHeaders(token?: string): HeadersInit {
  const headers = { ...defaultHeaders };

  if (token) {
    return {
      ...headers,
      'Authorization': `Bearer ${token}`,
    };
  }

  return headers;
}

// API client class for making requests

export class ApiClient {
  private baseURL: string;

  constructor(baseURL?: string) {
    this.baseURL = baseURL || getBaseURL();
  }

  // Generic request method
  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    const config: RequestInit = {
      headers: defaultHeaders,
      ...options,
    };

    let response = await fetch(url, config);

    // Handle 401 Unauthorized errors - try to refresh token first
    if (response.status === 401) {
      // Attempt to refresh the token
      const refreshResult = await refreshAuthToken();

      if (refreshResult) {
        // Token was refreshed successfully, retry the original request with the new token
        const newToken = refreshResult.token;
        if (newToken) {
          // Update the Authorization header with the new token
          const newConfig = {
            ...config,
            headers: {
              ...config.headers,
              'Authorization': `Bearer ${newToken}`,
            },
          };

          response = await fetch(url, newConfig);
        }
      }

      // If the request still fails with 401 after refresh, redirect to login
      if (response.status === 401) {
        handleUnauthorizedError();
        throw new Error('Unauthorized: Please log in again');
      }
    }

    if (!response.ok) {
      // Try to get error details from the response
      let errorMessage = `API request failed: ${response.status} ${response.statusText}`;
      try {
        const errorData = await response.json();
        if (errorData.message) {
          errorMessage = errorData.message;
        } else if (errorData.error) {
          errorMessage = errorData.error;
        }
      } catch (e) {
        // If we can't parse the error response, use the default message
        console.warn('Could not parse error response:', e);
      }

      throw new Error(errorMessage);
    }

    return response.json() as Promise<T>;
  }

  // GET request
  async get<T>(endpoint: string, token?: string): Promise<T> {
    const headers = getAuthHeaders(token);
    return this.request<T>(endpoint, { method: 'GET', headers });
  }

  // POST request
  async post<T>(endpoint: string, data?: any, token?: string): Promise<T> {
    const headers = getAuthHeaders(token);
    return this.request<T>(endpoint, {
      method: 'POST',
      headers,
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  // PUT request
  async put<T>(endpoint: string, data?: any, token?: string): Promise<T> {
    const headers = getAuthHeaders(token);
    return this.request<T>(endpoint, {
      method: 'PUT',
      headers,
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  // DELETE request
  async delete<T>(endpoint: string, token?: string): Promise<T> {
    const headers = getAuthHeaders(token);
    return this.request<T>(endpoint, { method: 'DELETE', headers });
  }

  // PATCH request
  async patch<T>(endpoint: string, data?: any, token?: string): Promise<T> {
    const headers = getAuthHeaders(token);
    return this.request<T>(endpoint, {
      method: 'PATCH',
      headers,
      body: data ? JSON.stringify(data) : undefined,
    });
  }
}

// Create a singleton instance of the API client
export const apiClient = new ApiClient();