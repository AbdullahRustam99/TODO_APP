// Focus management component for accessibility
import { useEffect, useRef, ReactNode } from 'react';

interface FocusManagerProps {
  children: ReactNode;
  autoFocus?: boolean;
  restoreFocus?: boolean;
  containerRef?: React.RefObject<HTMLDivElement>;
}

export const FocusManager = ({
  children,
  autoFocus = false,
  restoreFocus = true,
  containerRef: externalContainerRef
}: FocusManagerProps) => {
<<<<<<< HEAD
  const internalContainerRef = useRef<HTMLDivElement>(null);
=======
  const internalContainerRef = useRef<HTMLElement>(null);
>>>>>>> main
  const containerRef = externalContainerRef || internalContainerRef;
  const previousActiveElement = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (restoreFocus) {
      previousActiveElement.current = document.activeElement as HTMLElement;
    }

    if (autoFocus && containerRef.current) {
      // Try to focus on the first focusable element inside the container
      const focusableElement = containerRef.current.querySelector(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      ) as HTMLElement | null;

      if (focusableElement) {
        focusableElement.focus();
      } else {
        // If no focusable element is found, focus the container itself
        containerRef.current.focus();
      }
    }

    return () => {
      if (restoreFocus && previousActiveElement.current && previousActiveElement.current.focus) {
        previousActiveElement.current.focus();
      }
    };
  }, [autoFocus, restoreFocus]);

  return (
    <div
      ref={containerRef}
      tabIndex={-1}
      className="outline-none"
    >
      {children}
    </div>
  );
};