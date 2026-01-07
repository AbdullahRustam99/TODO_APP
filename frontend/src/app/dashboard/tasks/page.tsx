'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { TaskList } from '@/components/TaskList/TaskList';
import { TaskModal } from '@/components/TaskForm/TaskModal';
import { Button } from '@/components/UI/Button';
import { Task, CreateTaskRequest } from '@/lib/types';
import { useRouter } from 'next/navigation';
import { useTaskContext } from '@/context/TaskContext';
import { useTheme } from '@/context/ThemeContext';
import { Sidebar } from '@/components/UI/Sidebar';
import { cn } from '@/lib/utils';

export default function TasksPage() {
  const { user, logout } = useAuth();
  const { theme } = useTheme();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.replace('/');
  };
  const { createTask, updateTask, deleteTask, setCurrentView } = useTaskContext();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isVisible, setIsVisible] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    setIsVisible(true);
    setCurrentView('list');
  }, []); // Empty dependency array to run only once on mount


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
              <h1 className="text-xl font-bold">Tasks</h1>
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
          {/* Dashboard Title and Add Task Button */}
          <div className={`flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 sm:mb-8 animate-fade-in delay-150 ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
            <h2 className="text-2xl sm:text-3xl font-bold">Your Tasks</h2>
            <div className="w-full sm:w-auto">
              <Button
                variant="primary"
                onClick={handleAddTask}
                className="w-full flex items-center justify-center gap-2 animate-scale bg-gradient-to-r from-orange-500 to-yellow-500 hover:from-orange-600 hover:to-yellow-600 text-white shadow-lg shadow-orange-500/20"
                aria-label="Add new task"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                Add New Task
              </Button>
            </div>
          </div>

          {/* Task List with Filter Tabs */}
          <div className={`animate-fade-in delay-300 ${isVisible ? 'opacity-100' : 'opacity-0'}`} role="main">
            <TaskList
              onEditTask={handleEditTask}
              onDeleteTask={handleDeleteTask}
            />
          </div>

          {/* Task Modal */}
          <TaskModal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            onSubmit={handleTaskSubmit}
            editingTask={editingTask}
          />
        </main>
      </div>
    </div>
  );
}