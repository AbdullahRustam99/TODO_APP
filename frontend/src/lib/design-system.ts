/**
 * Design System Tokens
 * Consistent design tokens for the Todo App following the dark theme specification
 */

// Colors - Following the spec: Black (primary), Orange & Yellow (accent), supporting neutral grays
export const colors = {
  // Primary
  primary: {
    black: '#000000',
    black900: '#0a0a0a',
    black800: '#1a1a1a',
    black700: '#2a2a2a',
    black600: '#3a3a3a',
    black500: '#4a4a4a',
    black400: '#6a6a6a',
    black300: '#8a8a8a',
    black200: '#aaaaaa',
    black100: '#c9c9c9',
    black50: '#e9e9e9',
  },

  // Accents
  accent: {
    orange: '#f97316',      // Orange 500
    orange50: '#fff7ed',
    orange100: '#ffedd5',
    orange200: '#fed7aa',
    orange300: '#fdba74',
    orange400: '#fb923c',
    orange500: '#f97316',
    orange600: '#ea580c',
    orange700: '#c2410c',
    orange800: '#9a3412',
    orange900: '#7c2d12',

    yellow: '#eab308',      // Yellow 500
    yellow50: '#fefce8',
    yellow100: '#fef9c3',
    yellow200: '#fef08a',
    yellow300: '#fde047',
    yellow400: '#fbcf33',
    yellow500: '#eab308',
    yellow600: '#ca8a04',
    yellow700: '#a16207',
    yellow800: '#854d0e',
    yellow900: '#713f12',
  },

  // Neutral grays for the dark theme
  gray: {
    900: '#111827',
    800: '#1f2937',
    700: '#374151',
    600: '#4b5563',
    500: '#6b7280',
    400: '#9ca3af',
    300: '#d1d5db',
    200: '#e5e7eb',
    100: '#f3f4f6',
    50: '#f9fafb',
  },

  // Status colors
  status: {
    success: '#22c55e',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6',
  },
};

// Spacing - 8px grid system
export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '12px',
  lg: '16px',
  xl: '24px',
  '2xl': '32px',
  '3xl': '48px',
  '4xl': '64px',
};

// Typography
export const typography = {
  sizes: {
    xs: '0.75rem',  // 12px
    sm: '0.875rem', // 14px
    base: '1rem',   // 16px - minimum body text as per spec
    lg: '1.125rem', // 18px
    xl: '1.25rem',  // 20px
    '2xl': '1.5rem', // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem', // 36px
    '5xl': '3rem',  // 48px
    '6xl': '3.75rem', // 60px
  },
  weights: {
    thin: 100,
    extralight: 200,
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
    black: 900,
  },
  lineHeight: {
    none: '1',
    tight: '1.25',
    snug: '1.375',
    normal: '1.5',
    relaxed: '1.625',
    loose: '2',
  },
};

// Elevation - Soft shadows for different elevation levels
export const elevation = {
  none: 'none',
  sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
  base: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
  md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.05)',
  lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.05)',
  xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
};

// Radius - Consistent rounded corners (8px radius as standard)
export const radius = {
  sm: '4px',
  md: '8px',  // Standard as per spec
  lg: '12px',
  xl: '16px',
  '2xl': '24px',
  full: '9999px',
};

// Breakpoints for responsive design
export const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};

// Animation durations and easing
export const animations = {
  duration: {
    fast: '150ms',
    normal: '250ms',
    slow: '350ms',
    slowest: '500ms',
  },
  easing: {
    ease: 'ease',
    easeIn: 'ease-in',
    easeOut: 'ease-out',
    easeInOut: 'ease-in-out',
    linear: 'linear',
  },
};

// Z-index values
export const zIndex = {
  auto: 'auto',
  modal: '50',
  dropdown: '40',
  sticky: '30',
  header: '20',
  base: '0',
  below: '-10',
};