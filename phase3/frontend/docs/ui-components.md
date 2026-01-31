# UI Components Documentation

## Overview

This document describes all the UI components available in the Todo App frontend. Each component is designed to follow the design system guidelines and meet accessibility standards.

## Component Library

### Button Component

#### Props
- `variant`: `'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive'`
- `size`: `'sm' | 'md' | 'lg'`
- `loading`: `boolean` - Shows loading spinner
- `disabled`: `boolean` - Disables the button
- `className`: `string` - Additional CSS classes
- `children`: `ReactNode` - Button content

#### Usage
```jsx
<Button variant="primary" size="md">
  Click me
</Button>
```

#### Variants
- **Primary**: Main action button with orange background
- **Secondary**: Alternative action button with yellow background
- **Outline**: Transparent button with border
- **Ghost**: Minimal button with text only
- **Destructive**: Red button for destructive actions

#### Sizes
- **SM**: Small button (compact)
- **MD**: Medium button (default)
- **LG**: Large button (prominent)

### Input Component

#### Props
- `label`: `string` - Label text for the input
- `type`: `'text' | 'email' | 'password' | 'number' | 'date'` - Input type
- `placeholder`: `string` - Placeholder text
- `value`: `string` - Current value
- `onChange`: `(e: ChangeEvent) => void` - Value change handler
- `error`: `string` - Error message to display
- `as`: `'input' | 'textarea'` - Render as input or textarea
- `rows`: `number` - Number of rows for textarea
- `className`: `string` - Additional CSS classes

#### Usage
```jsx
<Input
  label="Email"
  type="email"
  placeholder="your@email.com"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={errors.email}
/>
```

### Card Component

#### Props
- `className`: `string` - Additional CSS classes
- `children`: `ReactNode` - Card content
- `variant`: `'default' | 'elevated' | 'outlined'` - Card style variant

#### Usage
```jsx
<Card>
  <CardContent>
    <h3>Card Title</h3>
    <p>Card content goes here</p>
  </CardContent>
</Card>
```

### Modal Component

#### Props
- `isOpen`: `boolean` - Controls modal visibility
- `onClose`: `() => void` - Callback when modal closes
- `title`: `string` - Modal title
- `children`: `ReactNode` - Modal content
- `className`: `string` - Additional CSS classes

#### Usage
```jsx
<Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Modal Title">
  <p>Modal content goes here</p>
</Modal>
```

### Toast Component

#### Props
- `message`: `string` - Toast message
- `type`: `'success' | 'error' | 'warning' | 'info'` - Toast type
- `isVisible`: `boolean` - Controls visibility
- `onClose`: `() => void` - Callback when toast closes
- `duration`: `number` - Auto-hide duration in ms

#### Usage
```jsx
<Toast
  message="Operation completed successfully"
  type="success"
  isVisible={showToast}
  onClose={() => setShowToast(false)}
/>
```

### Skeleton Component

#### Props
- `className`: `string` - Additional CSS classes
- `width`: `string | number` - Width of skeleton
- `height`: `string | number` - Height of skeleton
- `borderRadius`: `string` - Border radius

#### Usage
```jsx
<Skeleton height="20px" width="100%" borderRadius="8px" />
```

### Tooltip Component

#### Props
- `children`: `ReactNode` - Trigger element
- `content`: `ReactNode` - Tooltip content
- `position`: `'top' | 'right' | 'bottom' | 'left'` - Tooltip position
- `className`: `string` - Additional CSS classes

#### Usage
```jsx
<Tooltip content="This is a helpful tip" position="top">
  <button>Hover me</button>
</Tooltip>
```

### EmptyState Component

#### Props
- `title`: `string` - Title of the empty state
- `description`: `string` - Description text
- `illustration`: `ReactNode` - Optional illustration
- `action`: `ReactNode` - Optional call-to-action button
- `size`: `'sm' | 'md' | 'lg'` - Size of the empty state

#### Usage
```jsx
<EmptyState
  title="No tasks yet"
  description="Get started by creating your first task"
  action={<Button variant="primary">Create Task</Button>}
/>
```

## Task Components

### TaskItem Component

#### Props
- `task`: `Task` - Task object to display
- `onEdit`: `(task: Task) => void` - Edit callback
- `onDelete`: `(id: string) => void` - Delete callback

#### Usage
```jsx
<TaskItem
  task={task}
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

### TaskList Component

#### Props
- `onEditTask`: `(task: Task) => void` - Edit callback
- `onDeleteTask`: `(id: string) => void` - Delete callback

#### Usage
```jsx
<TaskList
  onEditTask={handleEditTask}
  onDeleteTask={handleDeleteTask}
/>
```

## AI Components

### AIAssistantPanel Component

#### Props
- `className`: `string` - Additional CSS classes

#### Usage
```jsx
<AIAssistantPanel className="w-full" />
```

### AISuggestionBadge Component

#### Props
- `size`: `'sm' | 'md' | 'lg'` - Badge size
- `className`: `string` - Additional CSS classes

#### Usage
```jsx
<AISuggestionBadge size="sm" />
```

## Layout Components

### Sidebar Component

#### Props
- `isOpen`: `boolean` - Controls sidebar visibility
- `onClose`: `() => void` - Close callback

#### Usage
```jsx
<Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
```

### SkipLink Component

#### Props
- `targetId`: `string` - ID of the target element to skip to
- `children`: `string` - Link text

#### Usage
```jsx
<SkipLink targetId="main-content">Skip to main content</SkipLink>
```

## Common Components

### ProgressBar Component

#### Props
- `value`: `number` - Current value (0-100)
- `max`: `number` - Maximum value (default 100)
- `label`: `string` - Label text
- `showPercentage`: `boolean` - Whether to show percentage
- `className`: `string` - Additional CSS classes
- `variant`: `'default' | 'success' | 'warning' | 'error'` - Style variant

#### Usage
```jsx
<ProgressBar value={75} label="Completion" variant="success" />
```

### FilterTabs Component

#### Props
- `tabs`: `Array<{ id: string; label: string; count?: number }>` - Tab definitions
- `activeTab`: `string` - Currently active tab
- `onTabChange`: `(tabId: string) => void` - Tab change callback
- `className`: `string` - Additional CSS classes

#### Usage
```jsx
<FilterTabs
  tabs={[
    { id: 'all', label: 'All', count: 10 },
    { id: 'active', label: 'Active', count: 5 },
    { id: 'completed', label: 'Completed', count: 5 }
  ]}
  activeTab={filter}
  onTabChange={setFilter}
/>
```

### ConfirmationDialog Component

#### Props
- `isOpen`: `boolean` - Controls dialog visibility
- `onClose`: `() => void` - Close callback
- `onConfirm`: `() => void` - Confirm callback
- `title`: `string` - Dialog title
- `message`: `string` - Dialog message
- `confirmText`: `string` - Confirm button text
- `cancelText`: `string` - Cancel button text
- `variant`: `'default' | 'destructive'` - Style variant
- `loading`: `boolean` - Shows loading state

#### Usage
```jsx
<ConfirmationDialog
  isOpen={showConfirm}
  onClose={() => setShowConfirm(false)}
  onConfirm={handleConfirm}
  title="Delete Task"
  message="Are you sure you want to delete this task?"
  confirmText="Delete"
  cancelText="Cancel"
  variant="destructive"
/>
```

### Breadcrumb Component

#### Props
- `items`: `Array<{ label: string; href?: string; active?: boolean }>` - Breadcrumb items
- `className`: `string` - Additional CSS classes

#### Usage
```jsx
<Breadcrumb
  items={[
    { label: 'Home', href: '/' },
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Tasks', active: true }
  ]}
/>
```

### Pagination Component

#### Props
- `currentPage`: `number` - Current page number
- `totalPages`: `number` - Total number of pages
- `onPageChange`: `(page: number) => void` - Page change callback
- `className`: `string` - Additional CSS classes

#### Usage
```jsx
<Pagination
  currentPage={currentPage}
  totalPages={totalPages}
  onPageChange={setCurrentPage}
/>
```

## Accessibility Components

### FocusManager Component

#### Props
- `children`: `ReactNode` - Managed content
- `autoFocus`: `boolean` - Whether to auto-focus
- `restoreFocus`: `boolean` - Whether to restore focus on unmount

#### Usage
```jsx
<FocusManager autoFocus>
  <div>Content that needs focus management</div>
</FocusManager>
```

## Component Composition

Many components can be composed together to create complex UI elements. For example:

```jsx
<Card>
  <CardHeader>
    <CardTitle>Task List</CardTitle>
    <CardDescription>Your current tasks</CardDescription>
  </CardHeader>
  <CardContent>
    <Input placeholder="Search tasks..." />
    <FilterTabs
      tabs={[
        { id: 'all', label: 'All', count: 10 },
        { id: 'active', label: 'Active', count: 5 }
      ]}
      activeTab="all"
      onTabChange={() => {}}
    />
    <TaskList
      onEditTask={() => {}}
      onDeleteTask={() => {}}
    />
  </CardContent>
</Card>
```

## Styling Guidelines

### CSS Classes
- Use Tailwind CSS utility classes wherever possible
- Use custom CSS only for complex animations or unique styling
- Follow BEM methodology for custom CSS classes
- Use CSS custom properties for theme values

### Responsive Design
- Use mobile-first approach
- Use appropriate breakpoints for different screen sizes
- Ensure all components are touch-friendly on mobile
- Test responsive behavior at all breakpoints

### Accessibility
- All interactive elements must be focusable
- Provide appropriate ARIA labels and roles
- Ensure sufficient color contrast
- Support keyboard navigation
- Include skip links for navigation

## Best Practices

### Performance
- Use React.memo for components that render frequently
- Implement proper key props for lists
- Use React.lazy for code splitting
- Optimize images and assets

### Accessibility
- Always include proper alt text for images
- Use semantic HTML elements
- Ensure proper heading hierarchy
- Include focus management for modals
- Support reduced motion preferences

### Internationalization
- Use translation keys instead of hardcoded text
- Support RTL languages
- Consider text expansion in UI design
- Format dates and numbers appropriately

### Error Handling
- Display user-friendly error messages
- Provide clear recovery options
- Log errors appropriately
- Show loading states for async operations