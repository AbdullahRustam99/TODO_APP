// Empty state component with illustration and actionable CTA
import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface EmptyStateProps {
  title: string;
  description: string;
  illustration?: ReactNode;
  action?: ReactNode;
  size?: 'sm' | 'md' | 'lg';
}

export const EmptyState = ({
  title,
  description,
  illustration,
  action,
  size = 'md'
}: EmptyStateProps) => {
  const sizeClasses = {
    sm: 'p-4',
    md: 'p-8',
    lg: 'p-12',
  }[size];

  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center text-center rounded-xl border border-gray-700',
        'bg-gray-800/30 backdrop-blur-sm',
        sizeClasses
      )}
      role="status"
      aria-live="polite"
    >
      {illustration && (
        <div className="mb-6 opacity-80" aria-hidden="true">
          {illustration}
        </div>
      )}
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-400 mb-6 max-w-md">{description}</p>
      {action && (
        <div className="animate-fade-in">
          {action}
        </div>
      )}
    </div>
  );
};