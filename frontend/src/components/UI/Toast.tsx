// Reusable Toast notification component with accessibility features
import { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';

interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'warning' | 'info';
  isVisible: boolean;
  onClose: () => void;
  duration?: number;
}

export const Toast = ({ message, type = 'info', isVisible, onClose, duration = 5000 }: ToastProps) => {
  const [show, setShow] = useState(isVisible);

  useEffect(() => {
    setShow(isVisible);
    if (isVisible) {
      const timer = setTimeout(() => {
        setShow(false);
        // Allow time for exit animation
        setTimeout(onClose, 300);
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [isVisible, duration, onClose]);

  if (!show) return null;

  const toastTypeClasses = cn({
    'bg-green-500/20 border-green-500/50 text-green-300': type === 'success',
    'bg-red-500/20 border-red-500/50 text-red-300': type === 'error',
    'bg-yellow-500/20 border-yellow-500/50 text-yellow-300': type === 'warning',
    'bg-blue-500/20 border-blue-500/50 text-blue-300': type === 'info',
  });

  return (
    <div
      className={cn(
        'fixed top-4 right-4 z-50 p-4 rounded-lg border backdrop-blur-sm transition-all duration-300',
        'animate-fade-in-up',
        toastTypeClasses
      )}
      role="alert"
      aria-live="assertive"
    >
      <div className="flex items-center justify-between">
        <span className="mr-2">{message}</span>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-white transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500 rounded-full p-1"
          aria-label="Close notification"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  );
};