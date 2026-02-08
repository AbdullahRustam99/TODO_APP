# Todo List App - Frontend

This is the frontend implementation of the Todo List App built with Next.js, TypeScript, and Tailwind CSS.

## Features

- **Authentication**: Secure login and signup with Better Auth
- **Task Management**: Create, read, update, and delete tasks
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Dark Theme**: Black, orange, and yellow color scheme
- **Accessibility**: WCAG 2.1 AA compliant
- **Form Validation**: Client-side validation with error handling

## Tech Stack

- Next.js 16+ (App Router)
- React 19
- TypeScript 5
- Tailwind CSS 4
- Better Auth for authentication
- clsx and tailwind-merge for class name utilities

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── layout.tsx       # Root layout with theme and auth providers
│   │   ├── page.tsx         # Home page (redirects to login/dashboard)
│   │   ├── login/           # Login page
│   │   ├── signup/          # Signup page
│   │   └── dashboard/       # Dashboard with task management
│   ├── components/          # Reusable UI components
│   │   ├── TaskList/        # Task list and item components
│   │   ├── TaskForm/        # Task form component
│   │   └── UI/              # Base UI components (Button, Input, Card)
│   ├── context/             # React context providers
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utilities and type definitions
│   └── styles/              # Global styles
├── tests/                   # Test files
└── docs/                    # Documentation
```

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Environment Variables

Create a `.env.local` file in the root of the frontend directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:3001/api
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3001
```

## Testing

Run the tests:
```bash
npm run test
```

## Key Implementation Details

### Authentication
- Uses Better Auth for secure authentication
- JWT tokens stored in localStorage
- Protected routes redirect unauthenticated users
- Auth context manages authentication state globally

### State Management
- Auth context for authentication state
- Theme context for dark/light mode
- Custom hooks for business logic (useTasks, useAuthHook)

### API Integration
- API client with JWT token attachment
- Error handling for API requests
- Mock implementations for demonstration

### UI Components
- Reusable Button, Input, and Card components
- TaskList and TaskItem for displaying tasks
- TaskForm for creating and updating tasks
- Responsive design with Tailwind CSS

### Accessibility Features
- Semantic HTML structure
- ARIA attributes for screen readers
- Keyboard navigation support
- Focus management
- Proper color contrast

### Responsive Design
- Mobile-first approach
- Responsive breakpoints for all screen sizes
- Flexible layouts using Tailwind CSS
