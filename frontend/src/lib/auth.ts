import { getBaseURL } from "@/lib/api";

// Authentication API functions
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
}

export interface AuthResponse {
  user: any;
  token: string;
  refresh_token?: string;
}

// Function to login user
export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  const response = await fetch(`${getBaseURL()}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail );
  }

  const data = await response.json();

  // Store both access and refresh tokens
  if (data.token) {
    setAuthToken(data.token);
  }
  if (data.refresh_token) {
    setRefreshToken(data.refresh_token);
  }

  return data;
};

// Function to register user
export const register = async (userData: RegisterData): Promise<AuthResponse> => {
  const response = await fetch(`${getBaseURL()}/api/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail);
  }

  const data = await response.json();

  // Store both access and refresh tokens
  if (data.token) {
    setAuthToken(data.token);
  }
  if (data.refresh_token) {
    setRefreshToken(data.refresh_token);
  }

  return data;
};

// Function to logout user
export const logout = async (token: string): Promise<void> => {
  await fetch(`${getBaseURL()}/api/auth/logout`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
};

// Function to get the JWT token from localStorage or cookies
export const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    // In browser environment
    return localStorage.getItem('auth-token');
  }
  return null;
};

// Function to get the refresh token from localStorage
export const getRefreshToken = (): string | null => {
  if (typeof window !== 'undefined') {
    // In browser environment
    return localStorage.getItem('refresh-token');
  }
  return null;
};

// Function to set the JWT token
export const setAuthToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth-token', token);
  }
};

// Function to set the refresh token
export const setRefreshToken = (refreshToken: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('refresh-token', refreshToken);
  }
};

// Function to remove the JWT token
export const removeAuthToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth-token');
    localStorage.removeItem('refresh-token'); // Also remove refresh token on logout
  }
};

// Function to refresh the access token using the refresh token
export const refreshAuthToken = async (): Promise<AuthResponse | null> => {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    return null;
  }

  try {
    const response = await fetch(`${getBaseURL()}/api/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) {
      // If refresh fails, remove both tokens
      removeAuthToken();
      return null;
    }

    const data: AuthResponse = await response.json();

    // Update both tokens in localStorage
    setAuthToken(data.token);
    if (data.refresh_token) {
      setRefreshToken(data.refresh_token);
    }

    return data;
  } catch (error) {
    console.error('Error refreshing token:', error);
    removeAuthToken(); // Remove tokens on error
    return null;
  }
};