// AI Assistant Panel component for the dashboard
'use client';

import { useState } from 'react';
import { useAI } from '@/context/AIContext';
import { Button } from '@/components/UI/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/UI/Card';
import { Input } from '@/components/UI/Input';
import { cn } from '@/lib/utils';

interface AIAssistantPanelProps {
  className?: string;
}

export const AIAssistantPanel = ({ className }: AIAssistantPanelProps) => {
  const { state, askAI, addToHistory } = useAI();
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    setIsLoading(true);

    try {
      // Add user message to history
      const userMessage = {
        id: Date.now().toString(),
        content: input,
        sender: 'user' as const,
        timestamp: new Date(),
      };
      addToHistory(userMessage);

      // Get AI response
      const response = await askAI(input);

      // Add AI response to history
      const aiMessage = {
        id: (Date.now() + 1).toString(),
        content: response,
        sender: 'ai' as const,
        timestamp: new Date(),
      };
      addToHistory(aiMessage);

      setInput('');
    } catch (error) {
      console.error('Error getting AI response:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className={cn("h-full flex flex-col", className)}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
          AI Assistant
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col">
        <div className="flex-1 mb-4 overflow-y-auto max-h-64 space-y-3">
          {state.history.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={cn(
                  'max-w-[80%] px-4 py-2 rounded-lg text-sm',
                  message.sender === 'user'
                    ? 'bg-orange-500 text-white rounded-br-none'
                    : 'bg-gray-700 text-gray-100 rounded-bl-none'
                )}
              >
                {message.content}
              </div>
            </div>
          ))}
          {state.isProcessing && (
            <div className="flex justify-start">
              <div className="bg-gray-700 text-gray-100 px-4 py-2 rounded-lg rounded-bl-none text-sm max-w-[80%]">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                </div>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask AI for help with tasks..."
            className="flex-1"
            disabled={isLoading}
          />
          <Button
            type="submit"
            variant="primary"
            disabled={isLoading || !input.trim()}
            className="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600"
          >
            {isLoading ? 'Thinking...' : 'Ask'}
          </Button>
        </form>

        <div className="mt-3 text-xs text-gray-400">
          <p>Suggestions: "Plan my day", "Show overdue tasks", "Create task"</p>
        </div>
      </CardContent>
    </Card>
  );
};