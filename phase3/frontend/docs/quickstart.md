# Quickstart Guide for AI-Powered Todo App

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn package manager
- Git version control system
- A modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo-app-frontend
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
```

### 3. Environment Configuration

Create a `.env.local` file in the root directory with the following variables:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_AI_API_BASE_URL=http://localhost:8001
NEXT_PUBLIC_AI_API_KEY=your_ai_api_key_here
```

### 4. Run the Development Server

```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`.

## Development Commands

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run start` - Start the production server
- `npm run lint` - Run ESLint for code quality checks
- `npm run test` - Run unit tests
- `npm run test:e2e` - Run end-to-end tests

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── layout.tsx       # Root layout with providers
│   │   ├── page.tsx         # Landing page
│   │   ├── login/page.tsx   # Login page
│   │   ├── signup/page.tsx  # Signup page
│   │   └── dashboard/page.tsx # Dashboard page
│   ├── components/          # Reusable UI components
│   │   ├── UI/              # Core UI components (Button, Input, Card, etc.)
│   │   ├── TaskList/        # Task-related components
│   │   ├── TaskForm/        # Task creation/editing forms
│   │   ├── AI/              # AI assistant components
│   │   └── Accessibility/   # Accessibility components
│   ├── context/             # React context providers
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utility functions and types
│   └── styles/              # CSS and design system files
├── public/                  # Static assets
├── docs/                    # Documentation files
└── tests/                   # Test files
```

## Key Features

### Authentication
- Secure login and signup flows
- JWT-based authentication
- Session management
- Protected routes

### Task Management
- Create, read, update, and delete tasks
- Task prioritization (high, medium, low)
- Due date tracking
- Completion status management
- Filtering and search capabilities

### AI Assistant
- AI-powered task suggestions
- Intelligent task prioritization
- Productivity insights
- Natural language processing for task creation

### Design System
- Consistent dark theme with orange/yellow accents
- Responsive layout for all device sizes
- Accessible components with WCAG 2.1 AA compliance
- Glassmorphism effects for dashboard components
- Smooth animations and transitions

## API Integration

The frontend communicates with the backend API located at `NEXT_PUBLIC_API_BASE_URL`. All API calls include proper authentication headers and error handling.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`npm run test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Troubleshooting

### Common Issues

1. **Module not found errors**: Run `npm install` to reinstall dependencies
2. **Environment variables not working**: Ensure `.env.local` is properly configured
3. **API calls failing**: Verify that the backend server is running and the API URL is correct
4. **Styles not loading**: Check that Tailwind CSS is properly configured

### Getting Help

- Check the documentation in the `docs/` directory
- Open an issue in the repository
- Contact the development team

## Next Steps

1. Explore the dashboard and familiarize yourself with the UI
2. Try creating and managing tasks
3. Experiment with the AI assistant features
4. Review the codebase to understand the implementation
5. Look at the documentation for detailed information about specific components