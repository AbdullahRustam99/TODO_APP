// Task form component
import { useState, useEffect } from 'react';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '@/lib/types';
import { Input } from '@/components/UI/Input';
import { Button } from '@/components/UI/Button';
import { Card, CardContent } from '@/components/UI/Card';
import { useTasks } from '@/hooks/useTasks';
import { useTheme } from '@/context/ThemeContext';
import { cn } from '@/lib/utils';
import { validateTaskForm } from '@/lib/validation';

interface TaskFormProps {
  task?: Task | null;
  onSubmit: (task: Task) => void;
  onCancel: () => void;
}

export const TaskForm = ({ task, onSubmit, onCancel }: TaskFormProps) => {
  const { createTask, updateTask } = useTasks();
  const { theme } = useTheme();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [completed, setCompleted] = useState(false);
  const [priority, setPriority] = useState<'high' | 'medium' | 'low'>('medium');
  const [dueDate, setDueDate] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  // Populate form when editing a task
  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description);
      setCompleted(task.completed);
      setPriority(task.priority || 'medium');
      setDueDate(task.dueDate || '');
    } else {
      // Reset form for new task
      setTitle('');
      setDescription('');
      setCompleted(false);
      setPriority('medium');
      setDueDate('');
    }
  }, [task]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const validation = validateTaskForm(title, description);

    if (!validation.isValid) {
      setErrors(validation.errors);
      setLoading(false);
      return;
    }

    // Clear previous errors
    setErrors({});

    try {
      if (task) {
        // Update existing task
        const updatedTask = await updateTask(task.id, {
          title,
          description,
          completed,
          priority,
          dueDate: dueDate || undefined,
        } as UpdateTaskRequest);
        onSubmit(updatedTask);
      } else {
        // Create new task
        const newTask = await createTask({
          title,
          description,
          completed,
          priority,
          dueDate: dueDate || undefined,
        } as CreateTaskRequest);
        onSubmit(newTask);
      }
    } catch (error) {
      console.error('Error saving task:', error);
      setErrors({ submit: 'Failed to save task. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className={cn(theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white')}>
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-4" role="form" aria-label={task ? "Update Task Form" : "Create Task Form"}>
          <div>
            <Input
              label="Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              error={errors.title}
              placeholder="Task title"
              required
              aria-required="true"
            />
          </div>

          <div>
            <Input
              label="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              error={errors.description}
              placeholder="Task description (optional)"
              as="textarea"
              rows={3}
            />
          </div>

          {/* Priority Selection */}
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-300">
              Priority
            </label>
            <div className="flex space-x-4">
              {(['high', 'medium', 'low'] as const).map((level) => (
                <label key={level} className="flex items-center">
                  <input
                    type="radio"
                    name="priority"
                    checked={priority === level}
                    onChange={() => setPriority(level)}
                    className="h-4 w-4 text-orange-500 focus:ring-orange-500"
                  />
                  <span className={`ml-2 text-sm capitalize ${
                    level === 'high' ? 'text-red-400' :
                    level === 'medium' ? 'text-yellow-400' : 'text-green-400'
                  }`}>
                    {level}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Due Date */}
          <div>
            <Input
              label="Due Date (optional)"
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              error={errors.dueDate}
              className="w-full"
            />
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="task-completed"
              checked={completed}
              onChange={(e) => setCompleted(e.target.checked)}
              className="h-4 w-4 rounded border-gray-300 text-orange-500 focus:ring-orange-500 focus:ring-2 focus:ring-offset-2 focus:ring-offset-background"
            />
            <label htmlFor="task-completed" className="ml-2 text-sm text-gray-300">
              Mark as completed
            </label>
          </div>

          {errors.submit && (
            <div className="text-red-500 text-sm" role="alert">{errors.submit}</div>
          )}

          <div className="flex flex-col sm:flex-row sm:justify-end sm:space-x-3 pt-4 gap-2 sm:gap-0">
            <Button
              type="button"
              variant="ghost"
              onClick={onCancel}
              disabled={loading}
              className="w-full sm:w-auto"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              loading={loading}
              className="w-full sm:w-auto"
            >
              {task ? 'Update Task' : 'Create Task'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};