'use client';

import { InputHTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  fullWidth?: boolean;
  animateOnChange?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, fullWidth = false, animateOnChange = true, className, ...props }, ref) => {
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

    return (
      <div className="w-full space-y-2">
        {label && (
          <label className="text-sm font-medium text-white">
            {label}
          </label>
        )}
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