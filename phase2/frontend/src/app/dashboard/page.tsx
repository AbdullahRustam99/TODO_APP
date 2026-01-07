'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { TaskList } from '@/components/TaskList/TaskList';
import { TaskModal } from '@/components/TaskForm/TaskModal';
import { Button } from '@/components/UI/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/UI/Card';
import { ProgressBar } from '@/components/UI/ProgressBar';
import { Task, CreateTaskRequest } from '@/lib/types';
import { useRouter } from 'next/navigation';
import { useTaskContext } from '@/context/TaskContext';
import { useTheme } from '@/context/ThemeContext';
import { Sidebar } from '@/components/UI/Sidebar';
import { AIAssistantPanel } from '@/components/AI/AIAssistantPanel';
import { cn } from '@/lib/utils';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const { theme } = useTheme();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.replace('/');
  };

  const { tasks, createTask, updateTask, deleteTask, setCurrentView } = useTaskContext();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isVisible, setIsVisible] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    setIsVisible(true);
    // Set current view to list for the dashboard (since dashboard view doesn't exist in context)
    setCurrentView('list');
  }, []); // Empty dependency array to run only once on mount

  // Calculate analytics data
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = tasks.filter(task => !task.completed).length;
  const overdueTasks = tasks.filter(task => {
    if (!task.dueDate) return false;
    return new Date(task.dueDate) < new Date() && !task.completed;
  }).length;
  const completionRate = tasks.length > 0 ? Math.round((completedTasks / tasks.length) * 100) : 0;

  const handleAddTask = () => {
    setEditingTask(null);
    setIsModalOpen(true);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const handleTaskSubmit = async (taskData: CreateTaskRequest & { id?: string; completed?: boolean }) => {
    try {
      if (editingTask) {
        // Update existing task via API
        await updateTask({
          ...editingTask,
          title: taskData.title,
          description: taskData.description,
          priority: taskData.priority || 'medium', // Default to medium if not provided
          dueDate: taskData.dueDate,
        });
      } else {
        // Create new task
        await createTask({
          title: taskData.title,
          description: taskData.description,
          completed: false, // New tasks start as incomplete
          priority: taskData.priority || 'medium', // Default to medium if not provided
          dueDate: taskData.dueDate,
        });
      }
      setIsModalOpen(false);
      setEditingTask(null);
    } catch (error) {
      console.error('Error saving task:', error);
    }
  };

  const handleDeleteTask = async (id: string) => {
    // Call the delete function from the useTasks hook
    try {
      await deleteTask(id);
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-[#0F0F0F] text-white flex">
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
              <h1 className="text-xl font-bold">Dashboard</h1>
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
          {/* Dashboard Overview Stats */}
          <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 animate-fade-in ${isVisible ? 'opacity-100' : 'opacity-0'}`} role="region" aria-labelledby="dashboard-heading">
            <h3 id="dashboard-heading" className="sr-only">Dashboard Overview</h3>

            <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm hover:shadow-xl transition-all duration-300 hover:shadow-orange-500/10 animate-slide-in-left">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-400">Total Tasks</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold text-orange-500">{tasks.length}</p>
                <p className="text-sm text-gray-500 mt-1">All tasks created</p>
              </CardContent>
            </Card>

            <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm hover:shadow-xl transition-all duration-300 hover:shadow-green-500/10 animate-slide-down">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-400">Completed</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold text-green-500">{completedTasks}</p>
                <p className="text-sm text-gray-500 mt-1">Tasks finished</p>
              </CardContent>
            </Card>

            <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm hover:shadow-xl transition-all duration-300 hover:shadow-yellow-500/10 animate-slide-in-right">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-400">Pending</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold text-yellow-500">{pendingTasks}</p>
                <p className="text-sm text-gray-500 mt-1">Tasks to complete</p>
              </CardContent>
            </Card>

            <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm hover:shadow-xl transition-all duration-300 hover:shadow-red-500/10 animate-slide-in-up">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-400">Overdue</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold text-red-500">{overdueTasks}</p>
                <p className="text-sm text-gray-500 mt-1">Tasks past due</p>
              </CardContent>
            </Card>
          </div>

          {/* Main Dashboard Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Task List Section */}
            <div className="lg:col-span-2">
              <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm animate-fade-in">
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-xl">Recent Tasks</CardTitle>
                    <Button variant="outline" size="sm" onClick={() => router.push('/dashboard/tasks')}>
                      View All
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <TaskList
                    onEditTask={handleEditTask}
                    onDeleteTask={handleDeleteTask}
                    limit={5}
                  />
                </CardContent>
              </Card>
            </div>

            {/* AI Assistant and Analytics Section */}
            <div className="space-y-6">
              {/* AI Assistant Panel */}
              <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm animate-fade-in">
                <CardHeader className="pb-4">
                  <CardTitle className="text-xl">AI Assistant</CardTitle>
                </CardHeader>
                <CardContent>
                  <AIAssistantPanel />
                </CardContent>
              </Card>

              {/* Completion Rate Card */}
              <Card className="bg-[#1C1C1C] border-gray-700 backdrop-blur-sm animate-fade-in delay-150">
                <CardHeader className="pb-4">
                  <CardTitle className="text-xl">Completion Rate</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center mb-4">
                    <div className="text-3xl font-bold text-orange-500 mb-1">{completionRate}%</div>
                    <div className="text-sm text-gray-400">of all tasks completed</div>
                  </div>
                  <ProgressBar
                    value={completionRate}
                    max={100}
                    className="bg-gray-700/50 h-3"
                    indicatorClassName="bg-gradient-to-r from-orange-500 to-yellow-500"
                  />
                  <div className="mt-3 text-sm text-gray-400">
                    {completionRate > 75 ? 'Excellent progress!' :
                     completionRate > 50 ? 'Good progress!' :
                     completionRate > 25 ? 'Keep going!' : 'Time to get started!'}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>

        {/* Task Modal */}
        <TaskModal
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setEditingTask(null);
          }}
          onSubmit={handleTaskSubmit}
          editingTask={editingTask}
        />
      </div>
    </div>
  );
}