import React, { InputHTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement | HTMLTextAreaElement> {
  label?: string;
  error?: string;
  fullWidth?: boolean;
  animateOnChange?: boolean;
  as?: 'input' | 'textarea';
  rows?: number; // Add rows prop for textarea
}

export const Input = React.forwardRef<HTMLInputElement | HTMLTextAreaElement, InputProps>(
  ({ label, error, fullWidth = false, animateOnChange = true, className, as = 'input', ...props }, ref) => {
    const baseClasses = 'flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm text-black file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200';

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

    const InputComponent = as === 'textarea' ? 'textarea' : 'input';

    return (
      <div className="space-y-2">
        {label && (
          <label className="text-sm font-medium text-white">
            {label}
          </label>
        )}
        <InputComponent
          ref={ref as any}
          className={classes}
          aria-invalid={!!error}
          aria-describedby={error ? `${props.id}-error` : undefined}
          {...props}
          value={props.value ?? ''}
        />
        {error && (
          <p
            id={props.id ? `${props.id}-error` : undefined}
            className="text-sm text-red-500"
          >
            {error}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';