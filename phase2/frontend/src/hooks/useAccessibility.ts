// Accessibility hook for keyboard navigation and focus management
import { useState, useEffect } from 'react';

interface AccessibilityState {
  isReducedMotion: boolean;
  isHighContrast: boolean;
  currentFocus: string | null;
  tabPressed: boolean;
}

export const useAccessibility = () => {
  const [state, setState] = useState<AccessibilityState>({
    isReducedMotion: false,
    isHighContrast: false,
    currentFocus: null,
    tabPressed: false,
  });

  // Check for reduced motion preference
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

    const handleChange = (e: MediaQueryListEvent) => {
      setState(prev => ({
        ...prev,
        isReducedMotion: e.matches,
      }));
    };

    setState(prev => ({
      ...prev,
      isReducedMotion: mediaQuery.matches,
    }));

    mediaQuery.addEventListener('change', handleChange);

    return () => {
      mediaQuery.removeEventListener('change', handleChange);
    };
  }, []);

  // Track focus changes
  useEffect(() => {
    const handleFocus = (e: FocusEvent) => {
<<<<<<< HEAD
      if (e.target && e.target instanceof HTMLElement) {
        const targetElement = e.target;
        setState(prev => ({
          ...prev,
          currentFocus: targetElement.tagName.toLowerCase() || targetElement.className || 'unknown',
=======
      if (e.target instanceof HTMLElement) {
        setState(prev => ({
          ...prev,
          currentFocus: e.target.tagName.toLowerCase() || e.target.className || 'unknown',
>>>>>>> main
        }));
      }
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        setState(prev => ({
          ...prev,
          tabPressed: true,
        }));
      }
    };

    document.addEventListener('focusin', handleFocus);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('focusin', handleFocus);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  // Function to manage focus in modals and dropdowns
  const manageFocus = (element: HTMLElement | null) => {
    if (element) {
      element.focus();
    }
  };

  // Function to trap focus within a container (useful for modals)
  const trapFocus = (container: HTMLElement, firstFocus?: HTMLElement) => {
    if (!container) return;

    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    ) as NodeListOf<HTMLElement>;

    const firstElement = firstFocus || focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey && document.activeElement === firstElement) {
        lastElement.focus();
        e.preventDefault();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        firstElement.focus();
        e.preventDefault();
      }
    };

    // Focus the first element when trapping starts
    firstElement?.focus();

    container.addEventListener('keydown', handleKeyDown);

    // Return cleanup function
    return () => {
      container.removeEventListener('keydown', handleKeyDown);
    };
  };

  return {
    ...state,
    manageFocus,
    trapFocus,
  };
};