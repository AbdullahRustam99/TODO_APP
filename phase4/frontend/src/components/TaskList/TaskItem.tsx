// Individual task item component with enhanced UI and animations
import { useState } from 'react';
import { Task } from '@/lib/types';
import { Button } from '@/components/UI/Button';
import { useTaskContext } from '@/context/TaskContext';
import { useTheme } from '@/context/ThemeContext';
import { AISuggestionBadge } from '@/components/AI/AISuggestionBadge';
import { ConfirmationDialog } from '@/components/Common/ConfirmationDialog';
import { cn } from '@/lib/utils';

interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

export const TaskItem = ({ task, onEdit, onDelete }: TaskItemProps) => {
  const { toggleTaskCompletion } = useTaskContext();
  const { theme } = useTheme();

  const handleToggleCompletion = async () => {
    try {
      await toggleTaskCompletion(task.id);
    } catch (error) {
      console.error('Error toggling task completion:', error);
    }
  };

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleDelete = () => {
    setShowDeleteConfirm(true);
  };

  const confirmDelete = () => {
    onDelete(task.id);
    setShowDeleteConfirm(false);
  };

  const cancelDelete = () => {
    setShowDeleteConfirm(false);
  };

  return (
    <div
      role="listitem"
      className={cn(
        'flex flex-col sm:flex-row items-start sm:items-center justify-between p-5 rounded-xl border mb-3 gap-4 transition-all duration-200 hover:shadow-lg hover:border-orange-500/30 animate-scale',
        theme === 'dark'
          ? 'bg-gray-800/70 border-gray-700'
          : 'bg-gray-800/70 border-gray-700',
        task.priority === 'high' && 'border-red-500/50',
        task.priority === 'medium' && 'border-yellow-500/50',
        task.priority === 'low' && 'border-green-500/50',
        task.completed && 'opacity-40 blur-[.7px]'
      )}
    >
      <div className="flex items-start space-x-4 flex-1 min-w-0">
        <div className="flex items-center pt-1">
          <input
            type="checkbox"
            id={`task-${task.id}-completed`}
            checked={task.completed}
            onChange={handleToggleCompletion}
            aria-label={`Mark task "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
            className={cn(
              "h-5 w-5 rounded border-2 focus:ring-2 focus:ring-offset-2 focus:ring-offset-background cursor-pointer",
              task.priority === 'high' ? 'border-red-500 text-red-500 focus:ring-red-500' :
              task.priority === 'medium' ? 'border-yellow-500 text-yellow-500 focus:ring-yellow-500' :
              'border-green-500 text-green-500 focus:ring-green-500'
            )}
          />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-3 mb-2">
            <h3
              className={cn(
                'text-base sm:text-lg font-medium transition-all duration-200 cursor-pointer',
                task.priority === 'high' ? 'text-red-400 hover:text-red-300' :
                task.priority === 'medium' ? 'text-yellow-400 hover:text-yellow-300' :
                'text-green-400 hover:text-green-300'
              )}
              onClick={handleToggleCompletion}
            >
              {task.title}
            </h3>
            {task.priority && (
              <span
                className={cn(
                  'inline-flex items-center px-3 py-1 rounded-full text-xs font-bold',
                  task.priority === 'high'
                    ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                    : task.priority === 'medium'
                      ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                      : 'bg-green-500/20 text-green-400 border border-green-500/30'
                )}
              >
                {task.priority.toUpperCase()}
              </span>
            )}
            {/* Show AI suggestion badge if task is AI-suggested */}
            {task.tags && task.tags.includes('ai-suggested') && (
              <AISuggestionBadge size="sm" />
            )}
          </div>
          <p
            className={cn(
              'text-sm mb-2 transition-all duration-200 text-gray-400'
            )}
          >
            {task.description}
          </p>
          {task.dueDate && (
            <div className="flex items-center text-xs text-gray-500 mt-1">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Due: {new Date(task.dueDate).toLocaleDateString()}
            </div>
          )}
        </div>
      </div>

      <div className="flex space-x-3 w-full sm:w-auto">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onEdit(task)}
          aria-label={`Edit task "${task.title}"`}
          className="flex-1 sm:flex-none animate-scale hover:border-orange-500 hover:text-orange-500"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Edit
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={handleDelete}
          aria-label={`Delete task "${task.title}"`}
          className="flex-1 sm:flex-none animate-scale hover:border-red-500 hover:text-red-500"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Delete
        </Button>
      </div>

      {/* Confirmation Dialog for Delete Action */}
      <ConfirmationDialog
        isOpen={showDeleteConfirm}
        onClose={cancelDelete}
        onConfirm={confirmDelete}
        title="Delete Task"
        message={`Are you sure you want to delete the task "${task.title}"? This action cannot be undone.`}
        confirmText="Delete"
        cancelText="Cancel"
        variant="destructive"
      />
    </div>
  );
};