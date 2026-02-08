// Loading spinner component for better UX
import { cn } from '@/lib/utils';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  color?: 'orange' | 'yellow' | 'blue' | 'white' | 'gray';
  className?: string;
  label?: string;
}

export const LoadingSpinner = ({
  size = 'md',
  color = 'orange',
  className,
  label = 'Loading...'
}: LoadingSpinnerProps) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16',
  };

  const colorClasses = {
    orange: 'text-orange-500',
    yellow: 'text-yellow-500',
    blue: 'text-blue-500',
    white: 'text-white',
    gray: 'text-gray-500',
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <div
        className={cn(
          "animate-spin rounded-full border-t-2 border-b-2 border-r-transparent border-l-transparent",
          sizeClasses[size],
          colorClasses[color],
          className
        )}
        role="status"
        aria-label={label}
      >
        <span className="sr-only">{label}</span>
      </div>
      {label && (
        <span className="mt-2 text-sm text-gray-400">{label}</span>
      )}
    </div>
  );
};