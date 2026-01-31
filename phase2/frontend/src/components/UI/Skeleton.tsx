// Reusable Skeleton loading component for better perceived performance
import { cn } from '@/lib/utils';

interface SkeletonProps {
  className?: string;
  width?: string | number;
  height?: string | number;
  borderRadius?: string;
}

export const Skeleton = ({
  className,
  width = '100%',
  height = '1rem',
  borderRadius = '0.5rem'
}: SkeletonProps) => {
  const style = {
    width: typeof width === 'number' ? `${width}px` : width,
    height: typeof height === 'number' ? `${height}px` : height,
    borderRadius,
  };

  return (
    <div
      className={cn(
        'animate-pulse bg-gray-700/50',
        'rounded-md',
        className
      )}
      style={style}
      aria-busy="true"
      aria-label="Loading content"
    />
  );
};