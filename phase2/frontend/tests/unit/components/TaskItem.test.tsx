import { render, screen, fireEvent } from '@testing-library/react';
import { TaskItem } from '@/components/TaskList/TaskItem';
import { Task } from '@/lib/types';

// Mock the useTasks hook
jest.mock('@/hooks/useTasks', () => ({
  useTasks: jest.fn(() => ({
    toggleTaskCompletion: jest.fn(),
  })),
}));

// Mock the useTheme hook
jest.mock('@/context/ThemeContext', () => ({
  useTheme: jest.fn(() => ({
    theme: 'dark',
  })),
}));

describe('TaskItem', () => {
  const mockTask: Task = {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    completed: false,
    createdAt: '2023-01-01T00:00:00Z',
    updatedAt: '2023-01-01T00:00:00Z',
    userId: 'user1',
  };

  const mockOnEdit = jest.fn();
  const mockOnDelete = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders task information correctly', () => {
    render(
      <TaskItem
        task={mockTask}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  it('calls onEdit when edit button is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /edit/i }));
    expect(mockOnEdit).toHaveBeenCalledWith(mockTask);
  });

  it('calls onDelete when delete button is clicked', () => {
    // Mock window.confirm to return true
    window.confirm = jest.fn(() => true);

    render(
      <TaskItem
        task={mockTask}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /delete/i }));
    expect(mockOnDelete).toHaveBeenCalledWith('1');
  });

  it('displays completed task with strikethrough', () => {
    const completedTask = { ...mockTask, completed: true };

    render(
      <TaskItem
        task={completedTask}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
      />
    );

    const titleElement = screen.getByText('Test Task');
    expect(titleElement).toHaveClass('line-through');
  });
});