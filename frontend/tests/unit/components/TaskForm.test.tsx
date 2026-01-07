import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { TaskForm } from '@/components/TaskForm/TaskForm';
import { Task } from '@/lib/types';

// Mock the useTasks hook
jest.mock('@/hooks/useTasks', () => ({
  useTasks: jest.fn(() => ({
    createTask: jest.fn(),
    updateTask: jest.fn(),
  })),
}));

// Mock the useTheme hook
jest.mock('@/context/ThemeContext', () => ({
  useTheme: jest.fn(() => ({
    theme: 'dark',
  })),
}));

describe('TaskForm', () => {
  const mockOnSubmit = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders form fields correctly', () => {
    render(
      <TaskForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByLabelText('Title')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toBeInTheDocument();
    expect(screen.getByLabelText('Mark as completed')).toBeInTheDocument();
  });

  it('allows user to input task details', () => {
    render(
      <TaskForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const titleInput = screen.getByLabelText('Title');
    const descriptionInput = screen.getByLabelText('Description');

    fireEvent.change(titleInput, { target: { value: 'New Task' } });
    fireEvent.change(descriptionInput, { target: { value: 'Task description' } });

    expect(titleInput).toHaveValue('New Task');
    expect(descriptionInput).toHaveValue('Task description');
  });

  it('calls onSubmit when form is submitted with valid data', async () => {
    const createTaskMock = jest.fn().mockResolvedValue({
      id: '1',
      title: 'New Task',
      description: 'Task description',
      completed: false,
      createdAt: '2023-01-01T00:00:00Z',
      updatedAt: '2023-01-01T00:00:00Z',
      userId: 'user1',
    });

    // Update mock to use the resolved value
    (require('@/hooks/useTasks').useTasks as jest.Mock).mockReturnValue({
      createTask: createTaskMock,
      updateTask: jest.fn(),
    });

    render(
      <TaskForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'New Task' } });
    fireEvent.change(screen.getByLabelText('Description'), { target: { value: 'Task description' } });

    fireEvent.click(screen.getByRole('button', { name: /create task/i }));

    await waitFor(() => {
      expect(createTaskMock).toHaveBeenCalledWith({
        title: 'New Task',
        description: 'Task description',
        completed: false,
      });
      expect(mockOnSubmit).toHaveBeenCalled();
    });
  });

  it('shows validation errors for empty title', async () => {
    render(
      <TaskForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: '' } });
    fireEvent.click(screen.getByRole('button', { name: /create task/i }));

    await waitFor(() => {
      expect(screen.getByText('This field is required')).toBeInTheDocument();
    });
  });
});