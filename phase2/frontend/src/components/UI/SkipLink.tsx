'use client';

import { useEffect } from 'react';

export const SkipLink = () => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // When Tab is pressed for the first time, show the skip link
      if (e.key === 'Tab' && !document.body.classList.contains('keyboard-navigation')) {
        document.body.classList.add('keyboard-navigation');
      }
    };

    const handleMouseDown = () => {
      // When mouse is used, remove the keyboard navigation class
      document.body.classList.remove('keyboard-navigation');
    };

    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('mousedown', handleMouseDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('mousedown', handleMouseDown);
    };
  }, []);

  const handleSkip = () => {
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
      mainContent.focus();
      mainContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <a
      href="#main-content"
      className="skip-link sr-only focus:not-sr-only focus:absolute"
      onClick={(e) => {
        e.preventDefault();
        handleSkip();
      }}
    >
      Skip to main content
    </a>
  );
};