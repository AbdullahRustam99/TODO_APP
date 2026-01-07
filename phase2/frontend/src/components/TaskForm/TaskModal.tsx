'use client';

import { useState, useEffect, useRef } from 'react';
import { Task, CreateTaskRequest } from '@/lib/types';
import { Button } from '@/components/UI/Button';
import { Input } from '@/components/UI/Input';
import { cn } from '@/lib/utils';

interface TaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (taskData: CreateTaskRequest & { id?: string; completed?: boolean }) => Promise<void>;
  editingTask?: Task | null;
}

export const TaskModal = ({ isOpen, onClose, onSubmit, editingTask }: TaskModalProps) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [priority, setPriority] = useState<'high' | 'medium' | 'low'>('medium');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const modalRef = useRef<HTMLDivElement>(null);

  // Populate form when editing a task
  useEffect(() => {
    if (editingTask) {
      setTitle(editingTask.title);
      setDescription(editingTask.description);
      setDueDate(editingTask.dueDate || '');
      setPriority(editingTask.priority || 'medium');
    } else {
      // Reset form for new task
      setTitle('');
      setDescription('');
      setDueDate('');
      setPriority('medium');
    }

    // Reset errors when opening/closing
    setErrors({});
  }, [editingTask, isOpen]);

  // Close modal on Escape key press
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose]);

  // Focus trap for accessibility
  useEffect(() => {
    if (isOpen && modalRef.current) {
      const focusableElements = modalRef.current.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );

      if (focusableElements.length > 0) {
        (focusableElements[0] as HTMLElement).focus();
      }
    }
  }, [isOpen]);

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!title.trim()) {
      newErrors.title = 'Title is required';
    } else if (title.trim().length < 3) {
      newErrors.title = 'Title must be at least 3 characters';
    } else if (title.trim().length > 100) {
      newErrors.title = 'Title must be less than 100 characters';
    }

    if (dueDate && new Date(dueDate) < new Date()) {
      newErrors.dueDate = 'Due date cannot be in the past';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setErrors({});

    try {
      const taskData = {
        title: title.trim(),
        description: description.trim(),
        priority,
        dueDate: dueDate ? dueDate : undefined,
        id: editingTask?.id,
        completed: editingTask?.completed,
      };

      // Pass raw form data to the parent component
      // The parent will handle the API call and state updates
      await onSubmit(taskData);
      setLoading(false);
      resetForm();
    } catch (error) {
      setErrors({ submit: 'Failed to save task. Please try again.' });
      setLoading(false);
    }
  };

  const resetForm = () => {
    setTitle('');
    setDescription('');
    setDueDate('');
    setPriority('medium');
    setErrors({});
  };

  // Close modal and reset form
  const handleClose = () => {
    onClose();
    resetForm();
  };

  // Handle outside click to close modal
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      handleClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
      onClick={handleBackdropClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="task-modal-title"
      aria-describedby="task-modal-description"
    >
      <div
        ref={modalRef}
        className={cn(
          "bg-gray-800 border border-gray-700 rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-300 ease-out",
          "scale-100 opacity-100",
          "focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-gray-900"
        )}
        role="document"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-700">
          <h2
            id="task-modal-title"
            className="text-xl font-bold text-white"
          >
            {editingTask ? 'Edit Task' : 'Create New Task'}
          </h2>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-white transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-orange-500 rounded-full p-1"
            aria-label="Close modal"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          <div>
            <Input
              label="Task Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              error={errors.title}
              placeholder="Enter task title"
              required
              aria-required="true"
              className="w-full"
              autoFocus
            />
          </div>

          <div>
            <Input
              label="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              error={errors.description}
              placeholder="Enter task description (optional)"
              as="textarea"
              rows={3}
              className="w-full"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Input
                label="Due Date"
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                error={errors.dueDate}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">
                Priority
              </label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as 'high' | 'medium' | 'low')}
                className={cn(
                  "w-full rounded-lg border border-gray-600 bg-gray-700 text-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent",
                  priority === 'high' ? 'border-red-500 bg-red-900/20' :
                  priority === 'medium' ? 'border-yellow-500 bg-yellow-900/20' : 'border-gray-500'
                )}
                aria-label="Select priority"
              >
                <option value="high" className="bg-gray-800 text-red-400">High</option>
                <option value="medium" className="bg-gray-800 text-yellow-400">Medium</option>
                <option value="low" className="bg-gray-800 text-gray-400">Low</option>
              </select>
            </div>
          </div>

          {errors.submit && (
            <div
              className="text-red-400 text-sm p-3 bg-red-900/20 rounded-lg border border-red-700"
              role="alert"
              aria-live="polite"
            >
              {errors.submit}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row-reverse gap-3 pt-2">
            <Button
              type="submit"
              variant="primary"
              className="w-full sm:w-auto bg-orange-500 hover:bg-orange-600 text-white"
              loading={loading}
              disabled={loading}
              aria-busy={loading}
            >
              {editingTask ? 'Update Task' : 'Add Task'}
            </Button>

            <Button
              type="button"
              variant="secondary"
              onClick={handleClose}
              className="w-full sm:w-auto border-gray-600 text-gray-300 hover:bg-gray-700"
              disabled={loading}
            >
              Cancel
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};