// API Health Check Component
// This component can be used to verify API connectivity and display the status

'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { useAuth } from '@/context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/UI/Card';
import { Button } from '@/components/UI/Button';

interface APIStatus {
  tasks: boolean;
  ai: boolean;
  auth: boolean;
  overall: boolean;
}

export const APIHealthCheck = () => {
  const { token } = useAuth();
  const [status, setStatus] = useState<APIStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  const checkAPIStatus = async () => {
    setLoading(true);

    try {
      // Test different API endpoints
      const tasksCheck = await testTasksAPI();
      const aiCheck = await testAIAPI();
      const authCheck = !!token; // Auth is considered working if token exists

      const overallStatus = tasksCheck && aiCheck && authCheck;

      setStatus({
        tasks: tasksCheck,
        ai: aiCheck,
        auth: authCheck,
        overall: overallStatus
      });
      setLastChecked(new Date());
    } catch (error) {
      console.error('API status check failed:', error);
      setStatus({
        tasks: false,
        ai: false,
        auth: !!token,
        overall: false
      });
      setLastChecked(new Date());
    } finally {
      setLoading(false);
    }
  };

  const testTasksAPI = async (): Promise<boolean> => {
    try {
      await apiClient.get('/api/tasks', token || undefined);
      return true;
    } catch (error) {
      console.error('Tasks API check failed:', error);
      return false;
    }
  };

  const testAIAPI = async (): Promise<boolean> => {
    try {
      await apiClient.get('/api/ai/suggestions', token || undefined);
      return true;
    } catch (error) {
      console.error('AI API check failed:', error);
      return false;
    }
  };

  useEffect(() => {
    checkAPIStatus();
  }, []);

  const getStatusColor = (isOk: boolean) => {
    return isOk ? 'text-green-500' : 'text-red-500';
  };

  const getStatusText = (isOk: boolean) => {
    return isOk ? 'Connected' : 'Disconnected';
  };

  return (
    <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-xl flex items-center justify-between">
          <span>API Health Status</span>
          <Button
            variant="outline"
            size="sm"
            onClick={checkAPIStatus}
            disabled={loading}
          >
            {loading ? 'Checking...' : 'Refresh'}
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex justify-between items-center p-3 bg-gray-800/30 rounded-lg">
            <span>Overall Status</span>
            <span className={`font-medium ${status ? getStatusColor(status.overall) : 'text-gray-500'}`}>
              {status ? getStatusText(status.overall) : 'Checking...'}
            </span>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between items-center p-2">
              <span className="text-sm">Tasks API</span>
              <span className={`text-sm font-medium ${status ? getStatusColor(status.tasks) : 'text-gray-500'}`}>
                {status ? getStatusText(status.tasks) : 'Checking...'}
              </span>
            </div>

            <div className="flex justify-between items-center p-2">
              <span className="text-sm">AI API</span>
              <span className={`text-sm font-medium ${status ? getStatusColor(status.ai) : 'text-gray-500'}`}>
                {status ? getStatusText(status.ai) : 'Checking...'}
              </span>
            </div>

            <div className="flex justify-between items-center p-2">
              <span className="text-sm">Auth Status</span>
              <span className={`text-sm font-medium ${status ? getStatusColor(status.auth) : 'text-gray-500'}`}>
                {status ? getStatusText(status.auth) : 'Checking...'}
              </span>
            </div>
          </div>

          {lastChecked && (
            <div className="text-xs text-gray-500 mt-4">
              Last checked: {lastChecked.toLocaleTimeString()}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};