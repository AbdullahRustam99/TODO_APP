// Reusable Tooltip component with accessibility features
import { useState, useEffect, useRef } from 'react';
import { cn } from '@/lib/utils';

interface TooltipProps {
  children: React.ReactNode;
  content: string;
  position?: 'top' | 'right' | 'bottom' | 'left';
}

export const Tooltip = ({ children, content, position = 'top' }: TooltipProps) => {
  const [visible, setVisible] = useState(false);
  const tooltipRef = useRef<HTMLDivElement>(null);
<<<<<<< HEAD
  const triggerRef = useRef<HTMLDivElement>(null);
=======
  const triggerRef = useRef<HTMLElement>(null);
>>>>>>> main

  // Handle visibility based on hover/focus
  useEffect(() => {
    const trigger = triggerRef.current;

    if (!trigger) return;

    const showTooltip = () => setVisible(true);
    const hideTooltip = () => setVisible(false);

    trigger.addEventListener('mouseenter', showTooltip);
    trigger.addEventListener('focus', showTooltip);
    trigger.addEventListener('mouseleave', hideTooltip);
    trigger.addEventListener('blur', hideTooltip);

    return () => {
      trigger.removeEventListener('mouseenter', showTooltip);
      trigger.removeEventListener('focus', showTooltip);
      trigger.removeEventListener('mouseleave', hideTooltip);
      trigger.removeEventListener('blur', hideTooltip);
    };
  }, []);

  // Position classes based on placement
  const positionClasses = {
    top: 'bottom-full left-1/2 transform -translate-x-1/2 mb-2',
    right: 'top-1/2 left-full transform -translate-y-1/2 ml-2',
    bottom: 'top-full left-1/2 transform -translate-x-1/2 mt-2',
    left: 'top-1/2 right-full transform -translate-y-1/2 mr-2',
  }[position];

  return (
    <div className="relative inline-block">
      <div ref={triggerRef} tabIndex={0} aria-describedby="tooltip">
        {children}
      </div>
      {visible && (
        <div
          ref={tooltipRef}
          id="tooltip"
          className={cn(
            'absolute z-50 px-3 py-2 text-sm font-medium text-white rounded-lg shadow-sm',
            'bg-gray-800 border border-gray-700 whitespace-nowrap',
            'animate-fade-in',
            positionClasses
          )}
          role="tooltip"
          aria-hidden="false"
        >
          {content}
          <div className="absolute w-2 h-2 bg-gray-800 rotate-45 border border-gray-700"
               style={{
                 [position === 'top' ? 'bottom' : position === 'bottom' ? 'top' : position === 'left' ? 'right' : 'left']: '-4px',
                 [position === 'top' || position === 'bottom' ? 'left' : 'top']: '50%',
                 transform: 'translateX(-50%) rotate(45deg)'
               }}></div>
        </div>
      )}
    </div>
  );
};