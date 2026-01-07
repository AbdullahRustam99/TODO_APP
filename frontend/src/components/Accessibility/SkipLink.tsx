// Skip link component for keyboard navigation accessibility
import { cn } from '@/lib/utils';

interface SkipLinkProps {
  targetId?: string;
  children?: string;
}

export const SkipLink = ({ targetId = 'main-content', children = 'Skip to main content' }: SkipLinkProps) => {
  return (
    <a
      href={`#${targetId}`}
      className={cn(
        'fixed top-4 left-4 z-[100] px-4 py-2 bg-orange-500 text-white rounded-lg shadow-lg',
        'focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-offset-2 focus:ring-offset-gray-900',
        'focus:bg-orange-600 focus:text-white',
        'transform -translate-y-full focus:translate-y-0 transition-transform duration-200',
        'border-2 border-transparent focus:border-orange-400'
      )}
    >
      {children}
    </a>
  );
};