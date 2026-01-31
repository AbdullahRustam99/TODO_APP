// AI Suggestion Badge component for highlighting AI-suggested tasks
import { cn } from '@/lib/utils';

interface AISuggestionBadgeProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const AISuggestionBadge = ({ className, size = 'md' }: AISuggestionBadgeProps) => {
  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-2.5 py-1.5',
    lg: 'text-base px-3 py-2',
  };

  return (
    <div
      className={cn(
        'inline-flex items-center gap-1 font-medium rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30',
        sizeClasses[size],
        className
      )}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className={cn(
          size === 'sm' ? 'h-3 w-3' : size === 'lg' ? 'h-5 w-5' : 'h-4 w-4'
        )}
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fillRule="evenodd"
          d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z"
          clipRule="evenodd"
        />
      </svg>
      <span>AI Suggested</span>
    </div>
  );
};