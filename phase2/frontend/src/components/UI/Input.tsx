'use client';

<<<<<<< HEAD
import { InputHTMLAttributes, TextareaHTMLAttributes, forwardRef } from 'react';
=======
import { InputHTMLAttributes, forwardRef } from 'react';
>>>>>>> main
import { cn } from '@/lib/utils';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  fullWidth?: boolean;
  animateOnChange?: boolean;
<<<<<<< HEAD
  as?: 'input' | 'textarea';
  rows?: number;
}

const Input = forwardRef<HTMLInputElement | HTMLTextAreaElement, InputProps>(
  ({ label, error, fullWidth = false, animateOnChange = true, className, as = 'input', rows, id, ...props }, ref) => {
    const baseClasses = 'flex w-full rounded-md border border-input bg-white px-3 py-2 text-sm text-black file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200';
=======
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, fullWidth = false, animateOnChange = true, className, ...props }, ref) => {
    const baseClasses = 'flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm text-black file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200';
>>>>>>> main

    const errorClasses = error ? 'border-red-500 focus-visible:ring-red-500' : '';
    const widthClass = fullWidth ? 'w-full' : '';

    // Animation classes when animateOnChange is enabled
    const animationClasses = animateOnChange ? 'focus:transform focus:scale-[1.02] transition-transform duration-200 ease-in-out' : '';

    const classes = cn(
      baseClasses,
      errorClasses,
      widthClass,
      animationClasses,
      className
    );

<<<<<<< HEAD
    const inputElement = as === 'textarea' ? (
      <textarea
        ref={ref as React.Ref<HTMLTextAreaElement>}
        className={`${classes} h-auto min-h-[40px]`}
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : undefined}
        rows={rows || 3}
        {...props as TextareaHTMLAttributes<HTMLTextAreaElement>}
      />
    ) : (
      <input
        ref={ref as React.Ref<HTMLInputElement>}
        className={classes}
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : undefined}
        {...props as InputHTMLAttributes<HTMLInputElement>}
      />
    );

=======
>>>>>>> main
    return (
      <div className="w-full space-y-2">
        {label && (
          <label className="text-sm font-medium text-white">
            {label}
          </label>
        )}
<<<<<<< HEAD
        {inputElement}
        {error && (
          <p
            id={id ? `${id}-error` : undefined}
=======
        <input
          ref={ref}
          className={classes}
          aria-invalid={!!error}
          aria-describedby={error ? `${props.id}-error` : undefined}
          {...props}
        />
        {error && (
          <p
            id={props.id ? `${props.id}-error` : undefined}
>>>>>>> main
            className="text-sm text-red-500"
          >
            {error}
          </p>
        )}
      </div>
    );
  }
);

<<<<<<< HEAD
Input.displayName = 'Input';

export { Input };
=======
Input.displayName = 'Input';
>>>>>>> main
