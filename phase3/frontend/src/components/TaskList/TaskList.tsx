// Task list component with enhanced UI and animations
import { useState } from 'react';
import { Task } from '@/lib/types';
import { TaskItem } from './TaskItem';
import { Input } from '@/components/UI/Input';
import { Button } from '@/components/UI/Button';
import { useTaskContext } from '@/context/TaskContext';
import { useTheme } from '@/context/ThemeContext';
import { FilterTabs } from '@/components/Common/FilterTabs';
import { cn } from '@/lib/utils';

interface TaskListProps {
  onEditTask: (task: Task) => void;
  onDeleteTask: (id: string) => void;
  limit?: number;
}

export const TaskList = ({ onEditTask, onDeleteTask, limit }: TaskListProps) => {
  const { tasks, loading, error, getTasksByStatus, searchTasks } = useTaskContext();
  const { theme } = useTheme();
  const [filter, setFilter] = useState<'all' | 'active' | 'completed' | 'priority'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  // Define priority order for sorting
  const priorityOrder = { high: 1, medium: 2, low: 3 };

  // Apply filters and search
  let filteredTasks = getTasksByStatus(filter);
  if (searchQuery) {
    filteredTasks = searchTasks(searchQuery);
  }

  // Sort tasks by priority
  filteredTasks.sort((a, b) => {
    const priorityA = a.priority ? priorityOrder[a.priority] : 4;
    const priorityB = b.priority ? priorityOrder[b.priority] : 4;
    return priorityA - priorityB;
  });


  // Apply limit if specified
  if (limit && !searchQuery && filter === 'all') { // Only apply limit when no search or filter
    filteredTasks = filteredTasks.slice(0, limit);
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-orange-500" role="status" aria-label="Loading tasks...">
          <span className="sr-only">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`p-4 rounded-lg ${theme === 'dark' ? 'bg-red-900/20 border border-red-700' : 'bg-red-100 border border-red-300'}`}>
        <p className="text-red-500" role="alert">Error: Failed to load tasks. Please try again later.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Search and Filter Controls */}
      <div className="space-y-4 animate-fade-in">
        <div className="flex flex-col sm:flex-row sm:items-center gap-4">
          <Input
            label="Search tasks"
            placeholder="Search tasks..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="sm:max-w-md animate-scale"
            aria-label="Search tasks"
          />
          <div>
            <FilterTabs
            tabs={[
              { id: 'all', label: 'All', count: tasks.length },
              { id: 'active', label: 'Active', count: tasks.filter(t => !t.completed).length },
              { id: 'completed', label: 'Completed', count: tasks.filter(t => t.completed).length },
              { id: 'priority', label: 'Priority', count: tasks.filter(t => t.priority === 'high' || t.priority === 'medium').length },
            ]}
            activeTab={filter}
            onTabChange={(tabId) => setFilter(tabId as 'all' | 'active' | 'completed' | 'priority')}
          />
          </div>
        </div>
      </div>

      {/* Task List */}
      <div role="list">
        {filteredTasks.length === 0 ? (
          <div className={`text-center py-12 rounded-lg ${theme === 'dark' ? 'bg-gray-800/50' : 'bg-gray-100'} animate-fade-in`}>
            <p className={cn('text-lg', theme === 'dark' ? 'text-gray-400' : 'text-gray-600')}>
              {searchQuery || filter !== 'all'
                ? filter === 'priority'
                  ? 'No high or medium priority tasks found.'
                  : 'No tasks match your search or filter criteria.'
                : 'No tasks yet. Add a new task to get started!'}
            </p>
          </div>
        ) : (
          <div className="space-y-3" role="list" aria-label="Task list">
            {filteredTasks.map((task, index) => (
              <div key={task.id} className={`animate-fade-in delay-${index * 100}`}>
                <TaskItem
                  task={task}
                  onEdit={onEditTask}
                  onDelete={onDeleteTask}
                />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};