// AI Task Optimizer component for suggesting task improvements
'use client';

import { useState } from 'react';
import { Button } from '@/components/UI/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/UI/Card';
import { useAI } from '@/context/AIContext';
import { Task } from '@/lib/types';
import { cn } from '@/lib/utils';

interface AITaskOptimizerProps {
  task: Task;
  onOptimize: (optimizedTask: Partial<Task>) => void;
  className?: string;
}

export const AITaskOptimizer = ({ task, onOptimize, className }: AITaskOptimizerProps) => {
  const { askAI } = useAI();
  const [isOptimizing, setIsOptimizing] = useState(false);

  const handleOptimize = async () => {
    setIsOptimizing(true);
    try {
      // In a real implementation, this would analyze the task and suggest improvements
      const suggestions = await askAI(`Optimize this task: ${task.title}. Provide suggestions for title, description, priority, and due date.`);

      // For now, we'll mock some optimizations
      const optimizedTask: Partial<Task> = {
        title: task.title,
        description: task.description ? task.description + " (AI optimized)" : "AI optimized description",
        priority: task.priority === 'low' ? 'medium' : task.priority, // Example optimization
      };

      onOptimize(optimizedTask);
    } catch (error) {
      console.error('Error optimizing task:', error);
    } finally {
      setIsOptimizing(false);
    }
  };

  return (
    <Card className={cn("bg-gray-800/50 border-gray-700", className)}>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium flex items-center gap-2">
          <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
          AI Task Optimizer
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-400 text-sm mb-3">
          Get AI suggestions to improve your task
        </p>
        <Button
          variant="outline"
          size="sm"
          onClick={handleOptimize}
          disabled={isOptimizing}
          className="w-full bg-blue-500/10 border-blue-500/30 hover:bg-blue-500/20 text-blue-400"
        >
          {isOptimizing ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Optimizing...
            </span>
          ) : (
            'Optimize Task'
          )}
        </Button>
      </CardContent>
    </Card>
  );
};