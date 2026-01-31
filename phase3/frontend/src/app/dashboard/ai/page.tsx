'use client';

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useTheme } from '@/context/ThemeContext';
import { Sidebar } from '@/components/UI/Sidebar';
import { Button } from '@/components/UI/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/UI/Card';
import { Input } from '@/components/UI/Input';
import { useTaskContext } from '@/context/TaskContext';
import { Task } from '@/lib/types';
import { useRouter } from 'next/navigation';
import { cn } from '@/lib/utils';
import { Chatbot } from '@/app/Chatbot';

export default function AIAssistantPage() {
  const { user, logout } = useAuth();
  const { theme } = useTheme();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.replace('/');
  };
  const { tasks, createTask, updateTask } = useTaskContext();
  const [messages, setMessages] = useState<Array<{id: string; content: string; sender: 'user' | 'ai'; timestamp: Date}>>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  useEffect(() => {
    setIsVisible(true);

    // Add welcome message
    setMessages([
      {
        id: 'welcome',
        content: "Hello! I'm your AI assistant. How can I help you with your tasks today?",
        sender: 'ai',
        timestamp: new Date(),
      }
    ]);
  }, []);


  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user' as const,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Simulate AI response with a delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Generate AI response based on user input
      let aiResponse = '';

      if (inputValue.toLowerCase().includes('suggest') || inputValue.toLowerCase().includes('recommend')) {
        // Generate task suggestions
        const suggestedTasks = [
          "Review quarterly reports",
          "Schedule team meeting for next week",
          "Update project documentation",
          "Follow up with client on proposal"
        ];

        aiResponse = `I suggest creating these tasks:\n${suggestedTasks.map((task, i) => `${i + 1}. ${task}`).join('\n')}\n\nWould you like me to create any of these tasks?`;
      } else if (inputValue.toLowerCase().includes('create') || inputValue.toLowerCase().includes('add')) {
        // Parse task creation request
        const titleMatch = inputValue.match(/(?:create|add|make)\s+(?:a\s+)?(?:task|todo|to-do)\s+(?:called|named|to)\s+"?([^"?\n]+)"?/i);
        const title = titleMatch ? titleMatch[1] : inputValue.replace(/(create|add|make)\s+(a\s+)?(task|todo|to-do)\s*/i, '').trim();

        if (title) {
          const newTask = await createTask({
            title,
            description: `Task created by AI assistant based on your request: "${inputValue}"`,
            completed: false,
            priority: 'medium',
          });

          aiResponse = `I've created the task "${title}" for you. It's been added to your task list.`;
        } else {
          aiResponse = "I can help you create a task. Try saying something like 'Create a task called Complete project report'";
        }
      } else if (inputValue.toLowerCase().includes('analyze') || inputValue.toLowerCase().includes('productivity')) {
        // Analyze user's productivity
        const completedTasks = tasks.filter(t => t.completed).length;
        const totalTasks = tasks.length;
        const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

        aiResponse = `I've analyzed your productivity:\n- Total tasks: ${totalTasks}\n- Completed: ${completedTasks}\n- Completion rate: ${completionRate}%\n\nYou're doing ${completionRate > 70 ? 'great' : completionRate > 50 ? 'well' : 'ok'}. Would you like suggestions to improve?`;
      } else {
        // Default AI response
        aiResponse = "I'm your AI assistant for task management. I can help you:\n- Create new tasks\n- Analyze your productivity\n- Suggest task priorities\n- Find tasks by keyword\n\nTry asking me to create a task or analyze your productivity!";
      }

      // Add AI response
      const aiMessage = {
        id: (Date.now() + 1).toString(),
        content: aiResponse,
        sender: 'ai' as const,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error getting AI response:', error);

      const errorMessage = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, I encountered an error processing your request. Please try again.",
        sender: 'ai' as const,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!user) {
    return null;
  }

  return (
    <div className="h-full bg-[#0F0F0F] text-white flex">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="border-b border-gray-700 bg-[#1C1C1C] backdrop-blur-sm sticky top-0 z-10 animate-fade-in">
          <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden mr-4 text-gray-400 hover:text-white focus:outline-none"
                aria-label="Toggle sidebar"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <h1 className="text-xl font-bold">AI Assistant</h1>
            </div>

            <div className="flex items-center space-x-4">
              {/* Notifications */}
              <button className="text-gray-400 hover:text-white relative" aria-label="Notifications">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>

              {/* User Profile */}
              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
                  <span className="text-sm font-medium">U</span>
                </div>
                <span className="ml-2 text-sm hidden md:block">{user?.name || user?.email}</span>
              </div>

              <Button
                variant="outline"
                onClick={handleLogout}
                className="ml-4 animate-scale"
                aria-label="Logout"
              >
                Logout
              </Button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main id="main-content" className="flex-1 overflow-y-auto p-6 focus:outline-none" tabIndex={-1}>
          <div className={`animate-fade-in ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
            <div className="max-w-4xl mx-auto">
              <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm h-[calc(100vh-200px)] flex flex-col">
                <CardHeader className="pb-4">
                  <CardTitle className="flex items-center gap-3">
                    <div className="p-2 bg-gradient-to-r from-orange-500 to-yellow-500 rounded-lg">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12h1m15.364-6.364l-.707-.707m0 15.364l-.707.707M4 12l1.414-1.414m0 11.314l-1.414-1.414m11.314-11.314l1.414-1.414m-11.314 11.314l1.414 1.414" />
                      </svg>
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold">AI Task Assistant</h2>
                      <p className="text-gray-400">Intelligent task management and productivity insights</p>
                    </div>
                  </CardTitle>
                </CardHeader>

                <CardContent className="flex-1 flex flex-col p-0">
                 <Chatbot/>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}