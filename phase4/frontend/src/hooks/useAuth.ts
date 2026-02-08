// Custom hook for authentication
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { LoginRequest, RegisterRequest } from '@/lib/types';
import { login as apiLogin, register as apiRegister } from '@/lib/auth';

export const useAuthHook = () => {
  const { user, token, login, logout } = useAuth();
  const router = useRouter();

  // Login function
  const handleLogin = async (credentials: LoginRequest) => {
    try {
      const response = await apiLogin({
        email: credentials.email,
        password: credentials.password,
      });

      // The response contains user data and token
      if (response && response.user && response.token) {
        login(response.user, response.token);
        router.push('/dashboard');
        return { success: true };
      } else {
        throw new Error('Invalid response from login API');
      }
    } catch (error) {
      console.error('Login error:', error);
      
      let errorMessage = 'Login failed. Please try again.';
      // Check for a detailed error message from the backend (e.g., from FastAPI HTTPException)
      if (error && typeof error === 'object' && 'response' in error &&
          error.response && typeof error.response === 'object' && 'data' in error.response &&
          error.response.data && typeof error.response.data === 'object' && 'detail' in error.response.data) {
        errorMessage = (error.response.data as any).detail;
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }
      
      return { success: false, error: errorMessage };
    }
  };

  // Register function
  const handleRegister = async (userData: RegisterRequest) => {
    try {
      const response = await apiRegister({
        email: userData.email,
        password: userData.password,
        name: userData.name || userData.email.split('@')[0], // Use email prefix as name if not provided
      });

      // The response contains user data and token
      if (response && response.user && response.token) {
        login(response.user, response.token);
        router.push('/dashboard');
        return { success: true };
      } else {
        throw new Error('Invalid response from register API');
      }
    } catch (error) {
      console.error('Registration error:', error);
      // Extract more specific error messages if available, ensure it's always a string
      let errorMessage = 'Registration failed';
      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      } else if (error && typeof error === 'object' && 'message' in error) {
        errorMessage = String((error as any).message) || JSON.stringify(error);
      } else if (error) {
        errorMessage = String(error);
      }
      return { success: false, error: errorMessage };
    }
  };

  // Logout function
  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  // Check if user is authenticated
  const isAuthenticated = !!user && !!token;

  return {
    user,
    token,
    isAuthenticated,
    handleLogin,
    handleRegister,
    handleLogout,
  };
};