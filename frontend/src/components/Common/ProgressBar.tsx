// Progress bar component for task completion visualization
import { cn } from '@/lib/utils';

interface ProgressBarProps {
  value: number; // 0-100
  max?: number;
  label?: string;
  showPercentage?: boolean;
  className?: string;
  variant?: 'default' | 'success' | 'warning' | 'error';
}

export const ProgressBar = ({
  value,
  max = 100,
  label,
  showPercentage = true,
  className,
  variant = 'default'
}: ProgressBarProps) => {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  const variantClasses = {
    default: 'bg-orange-500',
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    error: 'bg-red-500',
  };

  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between items-center mb-1">
          <span className="text-sm text-gray-400">{label}</span>
          {showPercentage && (
            <span className="text-sm text-gray-400">{percentage.toFixed(0)}%</span>
          )}
        </div>
      )}
      <div className={cn(
        "w-full h-2 bg-gray-700 rounded-full overflow-hidden",
        className
      )}>
        <div
          className={cn(
            "h-full rounded-full transition-all duration-500 ease-out",
            variantClasses[variant]
          )}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};