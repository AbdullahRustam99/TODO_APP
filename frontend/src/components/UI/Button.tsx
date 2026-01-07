// Reusable Button component with enhanced animations and design system
import { ButtonHTMLAttributes, ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  fullWidth?: boolean;
  animateOnHover?: boolean;
}

export const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  fullWidth = false,
  animateOnHover = true,
  className,
  disabled,
  ...props
}: ButtonProps) => {
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background';

  const variantClasses = cn({
    // Primary variant (orange background as per theme)
    'bg-orange-500 text-white hover:bg-orange-600': variant === 'primary',
    // Secondary variant (yellow background as per theme)
    'bg-yellow-500 text-black hover:bg-yellow-600': variant === 'secondary',
    // Outline variant (border with transparent background)
    'border border-gray-600 text-white hover:bg-gray-800': variant === 'outline',
    // Ghost variant (transparent with hover effect)
    'bg-transparent text-white hover:bg-gray-800': variant === 'ghost',
    // Destructive variant (for delete actions)
    'bg-red-500 text-white hover:bg-red-600': variant === 'destructive',
  });

  const sizeClasses = cn({
    'h-9 px-3 py-2 text-sm': size === 'sm',
    'h-10 px-4 py-2': size === 'md',
    'h-12 px-6 py-3 text-lg': size === 'lg',
  });

  const widthClass = fullWidth ? 'w-full' : '';

  // Animation classes when animateOnHover is enabled
  const animationClasses = animateOnHover ? 'hover:transform hover:scale-105 hover:shadow-lg transition-transform duration-200 ease-in-out' : '';

  const classes = cn(
    baseClasses,
    variantClasses,
    sizeClasses,
    widthClass,
    animationClasses,
    className
  );

  return (
    <button
      className={classes}
      disabled={disabled || loading}
      aria-busy={loading}
      {...props}
    >
      {loading ? (
        <span className="flex items-center">
          <svg
            className="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          <span aria-live="polite">Loading...</span>
        </span>
      ) : (
        children
      )}
    </button>
  );
};