// Validation utilities for the Todo App

// Email validation
export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Password validation
export const validatePassword = (password: string): boolean => {
  // At least 6 characters
  return password.length >= 6;
};

// Password match validation
export const validatePasswordMatch = (password: string, confirmPassword: string): boolean => {
  return password === confirmPassword;
};

// Task title validation
export const validateTaskTitle = (title: string): boolean => {
  // At least 3 characters and not more than 100
  return title.trim().length >= 3 && title.trim().length <= 100;
};

// Task description validation
export const validateTaskDescription = (description: string): boolean => {
  // Not more than 500 characters
  return description.length <= 500;
};

// Name validation
export const validateName = (name: string): boolean => {
  // At least 2 characters and not more than 50
  return name.trim().length >= 2 && name.trim().length <= 50;
};

// Validation error messages
export const getValidationMessage = (field: string, value: string | boolean = ''): string => {
  switch (field) {
    case 'email':
      return 'Please enter a valid email address';
    case 'password':
      return 'Password must be at least 6 characters long';
    case 'passwordMatch':
      return 'Passwords do not match';
    case 'taskTitle':
      return 'Task title must be at least 3 characters long';
    case 'taskDescription':
      return 'Task description must be less than 500 characters';
    case 'name':
      return 'Name must be at least 2 characters long';
    case 'required':
      return 'This field is required';
    default:
      return 'Invalid input';
  }
};

// Validation result type
export interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}

// Form validation functions
export const validateLoginForm = (email: string, password: string): ValidationResult => {
  const errors: Record<string, string> = {};

  if (!email) {
    errors.email = getValidationMessage('required');
  } else if (!validateEmail(email)) {
    errors.email = getValidationMessage('email');
  }

  if (!password) {
    errors.password = getValidationMessage('required');
  } else if (!validatePassword(password)) {
    errors.password = getValidationMessage('password');
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};

export const validateSignupForm = (
  name: string,
  email: string,
  password: string,
  confirmPassword: string
): ValidationResult => {
  const errors: Record<string, string> = {};

  if (!name) {
    errors.name = getValidationMessage('required');
  } else if (!validateName(name)) {
    errors.name = getValidationMessage('name');
  }

  if (!email) {
    errors.email = getValidationMessage('required');
  } else if (!validateEmail(email)) {
    errors.email = getValidationMessage('email');
  }

  if (!password) {
    errors.password = getValidationMessage('required');
  } else if (!validatePassword(password)) {
    errors.password = getValidationMessage('password');
  }

  if (!confirmPassword) {
    errors.confirmPassword = getValidationMessage('required');
  } else if (!validatePasswordMatch(password, confirmPassword)) {
    errors.confirmPassword = getValidationMessage('passwordMatch');
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};

export const validateTaskForm = (title: string, description: string): ValidationResult => {
  const errors: Record<string, string> = {};

  if (!title.trim()) {
    errors.title = getValidationMessage('required');
  } else if (!validateTaskTitle(title)) {
    errors.title = getValidationMessage('taskTitle');
  }

  if (description && !validateTaskDescription(description)) {
    errors.description = getValidationMessage('taskDescription');
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};