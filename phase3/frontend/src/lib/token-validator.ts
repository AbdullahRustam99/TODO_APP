// Token validation utilities
import { getAuthToken, removeAuthToken } from './auth';

// Check if JWT token is expired
export const isTokenExpired = (token: string): boolean => {
  try {
    // Split the token to get the payload
    const parts = token.split('.');
    if (parts.length !== 3) {
      return true; // Invalid token format
    }

    // Decode the payload (second part)
    const payload = parts[1];
    // Add padding if needed
    const paddedPayload = payload + '='.repeat((4 - payload.length % 4) % 4);
    const decodedPayload = atob(paddedPayload);
    const parsedPayload = JSON.parse(decodedPayload);

    // Check if the token has an expiration time
    if (!parsedPayload.exp) {
      return false; // No expiration, assume valid
    }

    // Check if the expiration time is in the past
    const currentTime = Math.floor(Date.now() / 1000);
    return parsedPayload.exp < currentTime;
  } catch (error) {
    console.error('Error validating token:', error);
    return true; // If we can't validate, assume it's expired
  }
};

// Validate the stored token and return if it's valid
export const validateStoredToken = (): boolean => {
  const token = getAuthToken();
  if (!token) {
    return false;
  }

  return !isTokenExpired(token);
};

// Remove token if it's expired
export const removeExpiredToken = (): void => {
  const token = getAuthToken();
  if (token && isTokenExpired(token)) {
    removeAuthToken();
    // Also remove user data
    if (typeof window !== 'undefined') {
      localStorage.removeItem('user');
    }
  }
};

// Check if token is about to expire (within 5 minutes)
export const isTokenExpiringSoon = (token: string, minutes: number = 5): boolean => {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      return true; // Invalid token format
    }

    const payload = parts[1];
    const paddedPayload = payload + '='.repeat((4 - payload.length % 4) % 4);
    const decodedPayload = atob(paddedPayload);
    const parsedPayload = JSON.parse(decodedPayload);

    if (!parsedPayload.exp) {
      return false; // No expiration, assume valid
    }

    const currentTime = Math.floor(Date.now() / 1000);
    const expiringSoonTime = currentTime + (minutes * 60); // Convert minutes to seconds
    return parsedPayload.exp < expiringSoonTime;
  } catch (error) {
    console.error('Error checking token expiration:', error);
    return true; // If we can't validate, assume it's expiring soon
  }
};