// API Integration Tests
// This file contains tests to verify that all API endpoints are properly connected

import { apiClient } from '@/lib/api';
import { getAuthToken } from '@/lib/auth';

// Test API integration for all pages
export const testAPIIntegration = async () => {
  const token = getAuthToken();
  const results: Record<string, any> = {};

  try {
    // Test tasks API
    console.log('Testing tasks API...');
    results.tasks = await apiClient.get('/api/tasks', token);
    console.log('✓ Tasks API test passed');
  } catch (error) {
    console.error('✗ Tasks API test failed:', error);
    results.tasks = { error: error instanceof Error ? error.message : 'Unknown error' };
  }

  try {
    // Test AI suggestions API
    console.log('Testing AI suggestions API...');
    results.aiSuggestions = await apiClient.get('/api/ai/suggestions', token);
    console.log('✓ AI suggestions API test passed');
  } catch (error) {
    console.error('✗ AI suggestions API test failed:', error);
    results.aiSuggestions = { error: error instanceof Error ? error.message : 'Unknown error' };
  }

  try {
    // Test AI query API
    console.log('Testing AI query API...');
    results.aiQuery = await apiClient.post('/api/ai/query', { query: 'test' }, token);
    console.log('✓ AI query API test passed');
  } catch (error) {
    console.error('✗ AI query API test failed:', error);
    results.aiQuery = { error: error instanceof Error ? error.message : 'Unknown error' };
  }

  try {
    // Test auth endpoints (if needed)
    console.log('Testing auth status...');
    results.auth = { token: !!token };
    console.log('✓ Auth test passed');
  } catch (error) {
    console.error('✗ Auth test failed:', error);
    results.auth = { error: error instanceof Error ? error.message : 'Unknown error' };
  }

  return results;
};

// Run API integration tests
export const runAPIIntegrationTests = async () => {
  console.log('Starting API integration tests...');
  const results = await testAPIIntegration();

  console.log('API Integration Test Results:', results);

  // Check if all tests passed
  const allPassed = !Object.values(results).some(result => result.error);

  if (allPassed) {
    console.log('✓ All API integration tests passed!');
  } else {
    console.log('✗ Some API integration tests failed');
  }

  return { allPassed, results };
};