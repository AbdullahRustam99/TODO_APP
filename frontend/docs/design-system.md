# Design System Documentation

## Overview

The Todo App design system provides a consistent and scalable foundation for the user interface. It ensures visual harmony, accessibility compliance, and developer efficiency across all components and pages.

## Color Palette

### Primary Colors
- **Background**: `#000000` (Pitch black)
- **Foreground**: `#FFFFFF` (White)
- **Card**: `#0A0A0A` (Dark gray-black)

### Accent Colors
- **Primary (Orange)**: `#F97316` - Used for primary actions, highlights, and active states
- **Secondary (Yellow)**: `#EAB308` - Used for secondary actions, warnings, and complementary elements
- **Accent**: `#1F2937` - Used for special highlights and emphasis

### Supporting Colors
- **Destructive**: `#EF4444` - Used for error states and destructive actions
- **Border**: `#374151` - Used for component borders
- **Input**: `#374151` - Used for input fields
- **Ring**: `#F97316` - Used for focus indicators

## Typography

### Font Family
- **Primary**: Inter (via Geist font stack)
- **Monospace**: Geist Mono for code and technical text

### Font Sizes
- **XS**: 12px (`0.75rem`)
- **SM**: 14px (`0.875rem`)
- **Base**: 16px (`1rem`) - Standard body text
- **LG**: 18px (`1.125rem`) - Secondary headings
- **XL**: 20px (`1.25rem`) - Primary headings
- **2XL**: 24px (`1.5rem`) - Section headings
- **3XL**: 30px (`1.875rem`) - Large headings
- **4XL**: 36px (`2.25rem`) - Hero headings
- **5XL**: 48px (`3rem`) - Large display text
- **6XL**: 60px (`3.75rem`) - Extra large display text

### Font Weights
- **Thin**: 100
- **Extra Light**: 200
- **Light**: 300
- **Normal**: 400
- **Medium**: 500
- **Semi Bold**: 600
- **Bold**: 700
- **Extra Bold**: 800
- **Black**: 900

### Line Heights
- **None**: 1
- **Tight**: 1.25
- **Snug**: 1.375
- **Normal**: 1.5
- **Relaxed**: 1.625
- **Loose**: 2

## Spacing System

### Grid System
- Based on 8px grid system with 4px increments
- Consistent rhythm and alignment across all components

### Spacing Scale
- **XS**: 4px (`0.25rem`)
- **SM**: 8px (`0.5rem`)
- **MD**: 16px (`1rem`) - Standard spacing unit
- **LG**: 24px (`1.5rem`)
- **XL**: 32px (`2rem`)
- **2XL**: 48px (`3rem`)
- **3XL**: 64px (`4rem`)
- **4XL**: 96px (`6rem`)
- **5XL**: 128px (`8rem`)
- **6XL**: 192px (`12rem`)
- **7XL**: 256px (`16rem`)

## Border Radius

### Radius Scale
- **XS**: 2px (`0.125rem`)
- **SM**: 4px (`0.25rem`)
- **MD**: 8px (`0.5rem`) - Standard component radius
- **LG**: 12px (`0.75rem`)
- **XL**: 16px (`1rem`)
- **2XL**: 24px (`1.5rem`)
- **3XL**: 32px (`2rem`)
- **Full**: Circular (9999px)

## Shadows

### Shadow Scale
- **SM**: Subtle shadow for depth (`0 1px 2px 0 rgba(0,0,0,0.05)`)
- **Default**: Standard shadow (`0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px -1px rgba(0,0,0,0.1)`)
- **MD**: Medium shadow for elevated components
- **LG**: Large shadow for prominent elements
- **XL**: Extra large shadow for modals
- **2XL**: Maximum shadow for floating elements

## Component Specifications

### Button Component
- **Primary**: Orange background with white text, medium font weight
- **Secondary**: Yellow background with black text
- **Outline**: Transparent background with orange border
- **Ghost**: Transparent background with text color only
- **Destructive**: Red background for dangerous actions
- **Sizes**: SM (small), MD (medium), LG (large)
- **States**: Default, hover, active, disabled, loading

### Input Component
- **Border**: 1px solid border with rounded corners
- **Focus**: Orange ring with 2px thickness and 2px offset
- **States**: Default, focus, error, disabled, success
- **Padding**: Consistent internal spacing

### Card Component
- **Background**: Semi-transparent dark background
- **Border**: Subtle border with accent color
- **Padding**: Consistent internal spacing
- **Shadow**: Appropriate shadow for elevation
- **Radius**: Rounded corners following design system

## Accessibility Standards

### Color Contrast
- All text elements meet WCAG 2.1 AA contrast ratios
- Minimum 4.5:1 ratio for normal text, 3:1 for large text

### Focus Management
- 2px focus ring with orange accent color
- 2px focus offset for clear visibility
- Visible focus indicators for all interactive elements
- Logical tab order following visual flow

### Reduced Motion
- Support for `prefers-reduced-motion` media query
- Animations disabled when user prefers reduced motion
- Smooth transitions for users who don't prefer reduced motion

### High Contrast Mode
- Support for `prefers-contrast: high` media query
- Enhanced contrast when high contrast mode is enabled

## Glassmorphism Effects

### Glass Card
- Semi-transparent background with backdrop blur
- Subtle border with light opacity
- Appropriate shadow for depth perception
- Used for dashboard analytics cards

### Frosted Glass
- Enhanced transparency with stronger blur effect
- Used for overlay panels and modal backgrounds
- Maintains readability while adding depth

## Animation Guidelines

### Duration
- **Fast**: 150ms for micro-interactions
- **Normal**: 250ms for standard transitions
- **Slow**: 350ms for significant state changes

### Easing
- `cubic-bezier(0.4, 0, 0.2, 1)` for most transitions
- `cubic-bezier(0.4, 0, 1, 1)` for ease-in
- `cubic-bezier(0, 0, 0.2, 1)` for ease-out
- `cubic-bezier(0.4, 0, 0.2, 1)` for ease-in-out

### Animation Types
- **Fade**: Opacity transitions for content appearance
- **Slide**: Position transitions for directional movement
- **Scale**: Size transitions for emphasis and interaction
- **Pulse**: Subtle animation for attention drawing
- **Bounce**: Playful animation for special cases

## Responsive Breakpoints

### Mobile First
- **Small (SM)**: 640px and above
- **Medium (MD)**: 768px and above
- **Large (LG)**: 1024px and above
- **Extra Large (XL)**: 1280px and above
- **2XL**: 1536px and above

## Theming

### Theme Variables
- `--background`: Background color
- `--foreground`: Text color
- `--primary`: Primary accent color
- `--secondary`: Secondary accent color
- `--accent`: Tertiary accent color
- `--destructive`: Error/danger color
- `--border`: Border color
- `--input`: Input field color
- `--ring`: Focus ring color
- `--radius`: Default border radius

### Theme Switching
- Supports light, dark, and system themes
- Automatic switching based on user preferences
- Smooth transitions between themes

## Component Categories

### UI Components
- **Button**: Interactive elements for actions
- **Input**: Text input fields with validation
- **Card**: Container for grouped content
- **Modal**: Overlay dialogs for important interactions
- **Toast**: Temporary notifications
- **Skeleton**: Loading placeholders
- **Tooltip**: Contextual help information
- **EmptyState**: Illustrations for empty content

### Layout Components
- **Header**: Top navigation and branding
- **Sidebar**: Vertical navigation menu
- **Main**: Primary content area
- **Footer**: Page footer information

### Task Components
- **TaskList**: Container for multiple tasks
- **TaskItem**: Individual task display
- **TaskForm**: Task creation and editing form
- **TaskModal**: Modal for task creation/editing

### AI Components
- **AIAssistantPanel**: Chat interface for AI assistant
- **AISuggestionBadge**: Visual indicator for AI-suggested tasks
- **AITaskOptimizer**: AI-powered task improvement suggestions

### Accessibility Components
- **SkipLink**: Jump navigation for keyboard users
- **FocusManager**: Focus management utilities
- **ScreenReaderText**: Hidden text for screen readers

## Implementation Guidelines

### Using the Design System
- Import components from the appropriate directories
- Use CSS custom properties for consistent theming
- Follow the established naming conventions
- Maintain accessibility standards in all implementations

### Extending the Design System
- Add new tokens to the appropriate CSS files
- Create new component variants following existing patterns
- Document new additions in this file
- Ensure new components meet accessibility standards

### Customization
- Override CSS custom properties for theme variations
- Extend components with additional classes as needed
- Maintain visual consistency when customizing
- Test customizations across all supported browsers and devices

## Testing and Validation

### Visual Regression Testing
- Components should be visually consistent across browsers
- Responsive behavior should be validated at all breakpoints
- Theme switching should be tested for all components

### Accessibility Testing
- All components should pass automated accessibility tests
- Keyboard navigation should be fully functional
- Screen reader compatibility should be verified
- Focus management should be tested thoroughly

### Performance Testing
- Components should render efficiently
- Animations should maintain 60fps performance
- Bundle sizes should be kept to a minimum
- Loading states should be implemented for async operations