# Frontend - Todo App

Next.js 14 frontend for the Todo App with TypeScript and Tailwind CSS.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS 3.x
- **Validation**: Zod 3.x
- **Authentication**: JWT tokens stored in localStorage

## Setup Instructions

### 1. Prerequisites

- Node.js 18 or higher
- npm package manager

### 2. Install Dependencies

```bash
npm install
```

### 3. Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

**Important**: Never commit the `.env.local` file to version control.

### 4. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Project Structure

```
frontend/
├── app/                 # Next.js App Router pages
│   ├── page.tsx         # Home page
│   ├── layout.tsx       # Root layout
│   ├── globals.css      # Global styles
│   ├── signin/          # Sign in page
│   ├── signup/          # Sign up page
│   └── tasks/           # Tasks page
│       └── page.tsx     # Task management page
├── components/          # React components
│   ├── Header.tsx       # Navigation header
│   ├── Footer.tsx       # Page footer
│   ├── TaskForm.tsx     # Task create/edit form
│   ├── TaskList.tsx     # Task list with pagination
│   ├── TaskItem.tsx     # Individual task display
│   └── Toast.tsx        # Toast notification component
├── lib/                 # Utility functions
│   ├── api.ts           # API client with JWT handling
│   ├── auth.tsx         # Authentication context
│   ├── types.ts         # TypeScript type definitions
│   └── toast.tsx        # Toast notification utilities
├── package.json         # Dependencies
└── .env.local           # Environment variables (not in git)
```

## Features

### Authentication

- User registration with email/password
- User sign in with JWT token
- Automatic token refresh
- Protected routes (redirect to sign in if not authenticated)

### Task Management

- **Create Tasks**: Add new tasks with title, description, and status
- **View Tasks**: Paginated list of all user's tasks
- **Edit Tasks**: Update task details inline
- **Delete Tasks**: Remove tasks with confirmation dialog
- **Status Management**: Track tasks as pending, in progress, or completed

### UI/UX Features

- Responsive design (mobile, tablet, desktop)
- Loading states with skeleton loaders
- Empty states with helpful messages
- Error handling with user-friendly messages
- Form validation with real-time feedback
- Character counters for text inputs
- Confirmation dialogs for destructive actions

## API Integration

The frontend communicates with the backend API using the `api` client in `lib/api.ts`.

All API requests automatically include:
- JWT token in `Authorization` header
- Proper error handling
- Session expiration detection

Example usage:

```typescript
import { api } from '@/lib/api';

// Create a task
const task = await api.createTask(userId, {
  title: 'Buy groceries',
  description: 'Milk, eggs, bread',
  status: TaskStatus.PENDING
});

// Get all tasks
const response = await api.getTasks(userId, page, pageSize);

// Update a task
const updated = await api.updateTask(userId, taskId, {
  status: TaskStatus.COMPLETED
});

// Delete a task
await api.deleteTask(userId, taskId);
```

## Authentication Flow

1. User signs up or signs in
2. Backend returns JWT token
3. Token is stored in localStorage
4. Token is automatically attached to all API requests
5. On 401 Unauthorized, user is redirected to sign in

## Styling

The app uses Tailwind CSS for styling. Key design principles:

- **Color Scheme**: Blue primary, gray neutrals, semantic colors for status
- **Typography**: System font stack for performance
- **Spacing**: Consistent spacing scale (4px base unit)
- **Responsive**: Mobile-first approach with breakpoints

## Type Safety

All API responses and component props are fully typed with TypeScript:

```typescript
// Task type
interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

// Task status enum
enum TaskStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
}
```

## Form Validation

Forms use Zod for schema validation:

```typescript
const taskSchema = z.object({
  title: z.string().min(1).max(500),
  description: z.string().max(2000).optional(),
  status: z.nativeEnum(TaskStatus).optional(),
});
```

Validation errors are displayed inline with helpful messages.

## Troubleshooting

### API Connection Error

```
Error: Failed to fetch
```

**Solution**: Verify NEXT_PUBLIC_API_URL in `.env.local` and ensure backend is running.

### Session Expired

```
Error: Session expired. Please sign in again.
```

**Solution**: JWT token has expired (24 hours). Sign in again to get a new token.

### Build Errors

```
Error: Module not found
```

**Solution**: Run `npm install` to ensure all dependencies are installed.

## Performance Optimization

- Server components by default (faster initial load)
- Client components only where needed (interactivity)
- Image optimization with Next.js Image component
- Code splitting with dynamic imports
- Lazy loading for off-screen content

## Accessibility

- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Focus management
- Color contrast compliance

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT
