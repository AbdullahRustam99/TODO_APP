// Drawer component for mobile navigation and modals
import { useEffect, useRef } from 'react';
import { cn } from '@/lib/utils';

interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
  position?: 'left' | 'right' | 'top' | 'bottom';
  size?: 'sm' | 'md' | 'lg' | 'full';
  className?: string;
}

export const Drawer = ({
  isOpen,
  onClose,
  children,
  position = 'left',
  size = 'md',
  className
}: DrawerProps) => {
  const drawerRef = useRef<HTMLDivElement>(null);

  // Close drawer when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (drawerRef.current && !drawerRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.body.style.overflow = ''; // Reset overflow
    };
  }, [isOpen, onClose]);

  // Handle ESC key press
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscKey);
    }

    return () => {
      document.removeEventListener('keydown', handleEscKey);
    };
  }, [isOpen, onClose]);

  // Size classes
  const sizeClasses = {
    sm: position === 'left' || position === 'right' ? 'w-64' : 'h-64',
    md: position === 'left' || position === 'right' ? 'w-80' : 'h-80',
    lg: position === 'left' || position === 'right' ? 'w-96' : 'h-96',
    full: position === 'left' || position === 'right' ? 'w-full' : 'h-full'
  };

  // Position classes
  const positionClasses = {
    left: `fixed top-0 h-full ${sizeClasses[size]} transform ${isOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 ease-in-out`,
    right: `fixed top-0 h-full ${sizeClasses[size]} transform ${isOpen ? 'translate-x-0' : 'translate-x-full'} transition-transform duration-300 ease-in-out`,
    top: `fixed left-0 w-full ${sizeClasses[size]} transform ${isOpen ? 'translate-y-0' : '-translate-y-full'} transition-transform duration-300 ease-in-out`,
    bottom: `fixed left-0 w-full ${sizeClasses[size]} transform ${isOpen ? 'translate-y-0' : 'translate-y-full'} transition-transform duration-300 ease-in-out`
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer */}
      <div
        ref={drawerRef}
        className={cn(
          positionClasses[position],
          'bg-[#1C1C1C] border-gray-700 z-50',
          position === 'left' || position === 'right' ? 'border-r' : 'border-t',
          className
        )}
        role="dialog"
        aria-modal="true"
        aria-labelledby="drawer-title"
      >
        <div className="h-full overflow-y-auto p-4">
          {children}
        </div>
      </div>
    </div>
  );
};