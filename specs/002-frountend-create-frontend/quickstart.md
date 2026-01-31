# Quickstart Guide: Phase II - Frontend UI

**Date**: 2025-12-29
**Feature**: Phase II - Frontend UI
**Input**: Implementation plan from `/specs/002-frountend-create-frontend/plan.md`

## Overview

This guide provides a quick setup and development workflow for the Phase II Frontend UI of the Todo App. The frontend is built with Next.js 16+, TypeScript, and Tailwind CSS, implementing comprehensive UI with landing page, authentication flows, and task CRUD interface.

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git for version control
- A code editor (VS Code recommended)

## Setup Instructions

### 1. Clone and Navigate to Frontend Directory
```bash
cd phase2/frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend directory with the following variables:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000/
```

### 4. Run Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## Key Development Commands

### Development
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run linter
npm run type-check   # Run TypeScript type checking
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── layout.tsx       # Root layout with theme
│   │   ├── page.tsx         # Landing page
│   │   ├── login/           # Login page
│   │   ├── signup/          # Signup page
│   │   └── dashboard/       # Dashboard page
│   ├── components/          # Reusable UI components
│   │   ├── Layout/          # Header, Sidebar
│   │   ├── TaskList/        # TaskList, TaskItem
│   │   ├── TaskForm/        # TaskForm
│   │   ├── Auth/            # LoginForm, SignupForm
│   │   └── UI/              # Button, Input, Card, Modal, Toast
│   ├── lib/                 # Utilities and API
│   │   ├── auth.ts          # Authentication utilities
│   │   ├── api.ts           # API client with JWT handling
│   │   └── types.ts         # TypeScript type definitions
│   ├── hooks/               # Custom React hooks
│   │   ├── useAuth.ts       # Authentication hook
│   │   └── useTasks.ts      # Task management hook
│   └── context/             # React Context providers
│       ├── AuthContext.tsx  # Authentication state management
│       └── ThemeContext.tsx # Theme management
```

## Key Features Implementation

### 1. Landing Page
- Located at `src/app/page.tsx`
- Implements dark-themed header with navigation
- Includes hero section with headline and CTA buttons
- Features cards for Fast & Simple, Smart Priorities, Secure Sync

### 2. Authentication Flow
- Signup page at `src/app/signup/page.tsx`
- Login page at `src/app/login/page.tsx`
- Integrates Better Auth for authentication
- Implements JWT token handling with secure storage
- Includes form validation with inline error messages

### 3. Task Management Dashboard
- Dashboard page at `src/app/dashboard/page.tsx`
- Implements CRUD operations for tasks
- Displays tasks with ID, title, description, and completion status
- Includes task actions: create, edit, delete, mark complete/incomplete
- Implements filter tabs: All, Active, Completed, Priority

### 4. API Integration
- API client in `src/lib/api.ts`
- Automatic JWT token attachment to requests
- Comprehensive error handling with user-friendly messages
- Proper handling of expired/invalid tokens

### 5. Component Architecture
- Reusable UI components in `src/components/`
- Custom hooks for business logic in `src/hooks/`
- Context providers for global state in `src/context/`
- Type definitions in `src/lib/types.ts`

## Styling and Theme

### Dark Theme Implementation
- Uses Tailwind CSS with dark mode configuration
- Color palette: black (primary), orange & yellow (accent)
- Rounded corners and soft shadows for modern UI
- High contrast ratios for accessibility

### Responsive Design
- Mobile-first approach with Tailwind's responsive utilities
- Properly sized touch targets for mobile devices
- Adapts to all screen sizes (mobile, tablet, desktop)

## Error Handling

### Client-Side Validation
- Form validation using react-hook-form
- Inline error messages for forms
- Non-technical language for user-friendly messages

### API Error Handling
- Toast notifications for global errors
- Proper handling of API errors (400, 401, 403, 500)
- Network error handling
- Graceful token expiration handling

## Testing

### Running Tests
```bash
npm run test          # Run all tests
npm run test:unit     # Run unit tests
npm run test:e2e      # Run end-to-end tests
```

## Deployment

### Build for Production
```bash
npm run build
npm run start
```

### Environment Variables for Production
Ensure the following environment variables are set:
- `NEXT_PUBLIC_API_BASE_URL`: Production API URL
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Production auth service URL