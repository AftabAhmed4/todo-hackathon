# Implementation Tasks: Task CRUD Operations

**Feature**: Task CRUD Operations
**Branch**: `001-task-crud`
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)
**Created**: 2026-01-12

## Overview

This document contains the complete implementation task list for the Task CRUD Operations feature, organized by user story to enable independent implementation and testing.

**Total Tasks**: 52
**MVP Scope**: User Story 1 + User Story 2 (Create and View Tasks)
**Parallel Opportunities**: 18 tasks marked with [P]

## Implementation Strategy

**Incremental Delivery by User Story**:
1. **Phase 1-2**: Setup and foundational infrastructure (blocking)
2. **Phase 3**: User Story 1 (P1) - Create New Task → First deployable increment
3. **Phase 4**: User Story 2 (P1) - View All Tasks → Complete MVP
4. **Phase 5**: User Story 3 (P2) - Update Existing Task → Enhancement
5. **Phase 6**: User Story 4 (P3) - Delete Task → Full feature set
6. **Phase 7**: Polish and cross-cutting concerns

**Independent Testing**: Each user story phase includes its own acceptance criteria and can be tested independently.

---

## Phase 1: Setup & Project Initialization

**Goal**: Initialize project structure, configure environment, and establish database connection.

**Tasks**:

- [X] T001 Verify backend/ directory exists with main.py, create if missing
- [X] T002 Verify frontend/ directory exists with package.json, create if missing
- [X] T003 Create backend/.env file with DATABASE_URL, BETTER_AUTH_SECRET, API_PORT, CORS_ORIGINS placeholders
- [X] T004 Create frontend/.env.local file with NEXT_PUBLIC_API_URL placeholder
- [X] T005 Update backend/requirements.txt to include: fastapi==0.104.1, sqlmodel==0.0.14, python-jose[cryptography]==3.3.0, passlib[bcrypt]==1.7.4, psycopg2-binary==2.9.9, uvicorn[standard]==0.24.0
- [X] T006 Install backend dependencies: pip install -r backend/requirements.txt
- [X] T007 Verify frontend dependencies include: next@14+, typescript@5+, tailwindcss@3+, zod@3+
- [X] T008 Install frontend dependencies: npm install (in frontend/ directory)

---

## Phase 2: Foundational Infrastructure (Blocking Prerequisites)

**Goal**: Implement shared infrastructure required by all user stories (database connection, authentication, base models).

**Tasks**:

- [X] T009 [P] Create backend/db.py with async database engine, session factory, and get_session dependency
- [X] T010 [P] Create backend/auth.py with JWT verification middleware: verify_token(), get_current_user() dependency
- [X] T011 [P] Create backend/models.py with TaskStatus enum (pending, in_progress, completed)
- [X] T012 Create backend/models.py Task model with fields: id (UUID), user_id (UUID, foreign key), title (str, max 500), description (Optional[str], max 2000), status (TaskStatus), created_at (datetime), updated_at (datetime)
- [X] T013 [P] Create backend/schemas.py with TaskCreate schema (title, description, status)
- [X] T014 [P] Create backend/schemas.py with TaskUpdate schema (Optional title, description, status)
- [X] T015 [P] Create backend/schemas.py with TaskRead schema (all Task fields)
- [X] T016 [P] Create backend/schemas.py with TaskListResponse schema (items, total, page, page_size, total_pages)
- [X] T017 Update backend/main.py to configure CORS middleware with allowed origins from environment
- [X] T018 Update backend/main.py to include startup event that creates database tables using SQLModel.metadata.create_all()
- [X] T019 [P] Create frontend/lib/types.ts with TaskStatus enum and Task, TaskCreate, TaskUpdate, TaskListResponse interfaces
- [X] T020 [P] Create frontend/lib/api.ts with base API client class that automatically attaches JWT token from Better Auth to all requests

---

## Phase 3: User Story 1 - Create New Task (Priority: P1)

**Story Goal**: Users can create new tasks with title and optional description.

**Independent Test**: Authenticate a user, submit task creation request with valid data, verify task appears in database with unique ID and correct user_id.

**Acceptance Criteria**:
- ✅ User can create task with title and description
- ✅ User can create task with only title (no description)
- ✅ System rejects task creation without title (validation error)
- ✅ Created task has unique ID and is associated with authenticated user

**Tasks**:

### Backend Implementation

- [X] T021 [US1] Create backend/routes/ directory if it doesn't exist
- [X] T022 [US1] Create backend/routes/tasks.py with APIRouter configured for prefix="/api/{user_id}/tasks"
- [X] T023 [US1] Implement POST /api/{user_id}/tasks endpoint in backend/routes/tasks.py that:
  - Accepts user_id path parameter and TaskCreate request body
  - Verifies user_id matches authenticated user from JWT (get_current_user dependency)
  - Returns 403 Forbidden if user_id mismatch
  - Creates new Task with user_id, title, description, status
  - Saves to database using SQLModel session
  - Returns 201 Created with TaskRead response
- [X] T024 [US1] Add input validation to POST endpoint: title required (1-500 chars), description optional (max 2000 chars)
- [X] T025 [US1] Add error handling to POST endpoint: return 400 Bad Request for validation errors with clear error messages
- [X] T026 [US1] Register tasks router in backend/main.py with app.include_router()

### Frontend Implementation

- [X] T027 [P] [US1] Implement createTask(userId, data) method in frontend/lib/api.ts that POSTs to /api/{user_id}/tasks with JWT token
- [X] T028 [P] [US1] Create frontend/components/TaskForm.tsx with form fields for title (required) and description (optional)
- [X] T029 [US1] Add client-side validation to TaskForm.tsx using Zod schema: title required (1-500 chars), description optional (max 2000 chars)
- [X] T030 [US1] Add form submission handler to TaskForm.tsx that calls api.createTask() and handles success/error states
- [X] T031 [US1] Add loading state indicator to TaskForm.tsx during submission
- [X] T032 [US1] Add error display to TaskForm.tsx for validation and API errors
- [X] T033 [US1] Create frontend/app/tasks/page.tsx with TaskForm component for creating new tasks

### Integration & Verification

- [X] T034 [US1] Test POST /api/{user_id}/tasks endpoint with valid data returns 201 and task details
- [X] T035 [US1] Test POST endpoint rejects empty title with 400 validation error
- [X] T036 [US1] Test POST endpoint rejects user_id mismatch with 403 Forbidden
- [X] T037 [US1] Test frontend TaskForm successfully creates task and displays success message

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Story Goal**: Users can view a list of all their tasks with pagination.

**Independent Test**: Create multiple tasks for a user, retrieve task list, verify only their tasks are returned (not other users' tasks), verify pagination works correctly.

**Acceptance Criteria**:
- ✅ User can view all their tasks
- ✅ Empty list returned if user has no tasks
- ✅ User only sees their own tasks (data isolation)
- ✅ Pagination works correctly (20 items per page default)

**Tasks**:

### Backend Implementation

- [X] T038 [US2] Implement GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py that:
  - Accepts user_id path parameter, page (default 1) and page_size (default 20) query parameters
  - Verifies user_id matches authenticated user from JWT
  - Returns 403 Forbidden if user_id mismatch
  - Queries tasks filtered by user_id with pagination (LIMIT/OFFSET)
  - Counts total tasks for user
  - Returns 200 OK with TaskListResponse (items, total, page, page_size, total_pages)
- [X] T039 [US2] Add query optimization to GET endpoint: order tasks by created_at DESC
- [X] T040 [US2] Add pagination validation to GET endpoint: page >= 1, page_size between 1-100
- [X] T041 [US2] Add error handling to GET endpoint: return 400 Bad Request for invalid pagination parameters

### Frontend Implementation

- [X] T042 [P] [US2] Implement getTasks(userId, page, pageSize) method in frontend/lib/api.ts that GETs from /api/{user_id}/tasks with JWT token
- [X] T043 [P] [US2] Create frontend/components/TaskItem.tsx to display individual task (title, description, status, timestamps)
- [X] T044 [US2] Create frontend/components/TaskList.tsx that:
  - Fetches tasks using api.getTasks()
  - Displays loading state while fetching
  - Renders TaskItem for each task
  - Displays empty state if no tasks
  - Handles errors with user-friendly messages
- [X] T045 [US2] Add pagination controls to TaskList.tsx (Previous/Next buttons, page indicator)
- [X] T046 [US2] Update frontend/app/tasks/page.tsx to include TaskList component below TaskForm

### Integration & Verification

- [X] T047 [US2] Test GET /api/{user_id}/tasks endpoint returns all user's tasks with correct pagination metadata
- [X] T048 [US2] Test GET endpoint returns empty list for user with no tasks
- [X] T049 [US2] Test GET endpoint enforces data isolation (user A cannot see user B's tasks)
- [X] T050 [US2] Test frontend TaskList successfully displays tasks and handles pagination

---

## Phase 5: User Story 3 - Update Existing Task (Priority: P2)

**Story Goal**: Users can modify title, description, and status of their existing tasks.

**Independent Test**: Create a task, update its fields, verify changes are persisted and reflected in subsequent retrievals.

**Acceptance Criteria**:
- ✅ User can update task title, description, and status
- ✅ Partial updates work (update only one field)
- ✅ System rejects updates to tasks user doesn't own (403 Forbidden)
- ✅ System rejects updates with invalid task ID (404 Not Found)
- ✅ System rejects updates with empty title (validation error)

**Tasks**:

### Backend Implementation

- [X] T051 [US3] Implement GET /api/{user_id}/tasks/{task_id} endpoint in backend/routes/tasks.py that:
  - Accepts user_id and task_id path parameters
  - Verifies user_id matches authenticated user from JWT
  - Returns 403 Forbidden if user_id mismatch
  - Queries task by id and user_id
  - Returns 404 Not Found if task doesn't exist or doesn't belong to user
  - Returns 200 OK with TaskRead response
- [X] T052 [US3] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in backend/routes/tasks.py that:
  - Accepts user_id, task_id path parameters and TaskUpdate request body
  - Verifies user_id matches authenticated user from JWT
  - Returns 403 Forbidden if user_id mismatch
  - Queries task by id and user_id
  - Returns 404 Not Found if task doesn't exist or doesn't belong to user
  - Updates only provided fields (partial update)
  - Updates updated_at timestamp
  - Returns 200 OK with updated TaskRead response
- [X] T053 [US3] Add input validation to PUT endpoint: if title provided, must be 1-500 chars; if description provided, max 2000 chars
- [X] T054 [US3] Add error handling to PUT endpoint: return 400 Bad Request for validation errors

### Frontend Implementation

- [X] T055 [P] [US3] Implement getTask(userId, taskId) method in frontend/lib/api.ts that GETs from /api/{user_id}/tasks/{task_id}
- [X] T056 [P] [US3] Implement updateTask(userId, taskId, data) method in frontend/lib/api.ts that PUTs to /api/{user_id}/tasks/{task_id}
- [X] T057 [US3] Update TaskForm.tsx to support edit mode: accept optional task prop, pre-fill form fields if task provided
- [X] T058 [US3] Update TaskForm.tsx submission handler to call api.updateTask() when in edit mode
- [X] T059 [US3] Add status dropdown to TaskForm.tsx with options: pending, in_progress, completed
- [X] T060 [US3] Create frontend/app/tasks/[id]/page.tsx for task detail/edit view with TaskForm in edit mode
- [X] T061 [US3] Add "Edit" button to TaskItem.tsx that navigates to /tasks/[id] page

### Integration & Verification

- [X] T062 [US3] Test GET /api/{user_id}/tasks/{task_id} endpoint returns task details for valid task
- [X] T063 [US3] Test GET endpoint returns 404 for non-existent or unauthorized task
- [X] T064 [US3] Test PUT /api/{user_id}/tasks/{task_id} endpoint successfully updates task fields
- [X] T065 [US3] Test PUT endpoint supports partial updates (update only title, only description, only status)
- [X] T066 [US3] Test PUT endpoint rejects empty title with 400 validation error
- [X] T067 [US3] Test PUT endpoint rejects unauthorized updates with 403/404
- [X] T068 [US3] Test frontend task edit page successfully updates task and displays changes

---

## Phase 6: User Story 4 - Delete Task (Priority: P3)

**Story Goal**: Users can permanently delete tasks they no longer need.

**Independent Test**: Create a task, delete it, verify it no longer appears in task list and cannot be retrieved by ID.

**Acceptance Criteria**:
- ✅ User can delete their own tasks
- ✅ System rejects deletion of tasks user doesn't own (403 Forbidden)
- ✅ System rejects deletion with invalid task ID (404 Not Found)
- ✅ Deleted task cannot be retrieved afterward

**Tasks**:

### Backend Implementation

- [X] T069 [US4] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/routes/tasks.py that:
  - Accepts user_id and task_id path parameters
  - Verifies user_id matches authenticated user from JWT
  - Returns 403 Forbidden if user_id mismatch
  - Queries task by id and user_id
  - Returns 404 Not Found if task doesn't exist or doesn't belong to user
  - Deletes task from database
  - Returns 200 OK with success message and deleted task ID
- [X] T070 [US4] Add error handling to DELETE endpoint for database errors

### Frontend Implementation

- [X] T071 [P] [US4] Implement deleteTask(userId, taskId) method in frontend/lib/api.ts that DELETEs /api/{user_id}/tasks/{task_id}
- [X] T072 [US4] Add "Delete" button to TaskItem.tsx with confirmation dialog
- [X] T073 [US4] Add delete handler to TaskItem.tsx that calls api.deleteTask() and removes task from list on success
- [X] T074 [US4] Add loading state to delete button during deletion
- [X] T075 [US4] Add error handling to delete operation with user-friendly error messages

### Integration & Verification

- [X] T076 [US4] Test DELETE /api/{user_id}/tasks/{task_id} endpoint successfully deletes task
- [X] T077 [US4] Test DELETE endpoint returns 404 for non-existent or unauthorized task
- [X] T078 [US4] Test deleted task cannot be retrieved via GET endpoint (returns 404)
- [X] T079 [US4] Test deleted task does not appear in task list
- [X] T080 [US4] Test frontend delete button successfully removes task from UI

---

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Add final touches, error handling improvements, and production readiness.

**Tasks**:

### Error Handling & Validation

- [X] T081 [P] Add global exception handler to backend/main.py for HTTPException with consistent JSON error format
- [X] T082 [P] Add global exception handler to backend/main.py for unexpected errors (500 Internal Server Error)
- [X] T083 [P] Add request logging middleware to backend/main.py for debugging and audit trail
- [X] T084 [P] Add error boundary to frontend/app/layout.tsx for graceful error handling

### UI/UX Improvements

- [X] T085 [P] Add loading skeleton to TaskList.tsx for better perceived performance
- [X] T086 [P] Add toast notifications to frontend for success/error messages (create, update, delete operations)
- [X] T087 [P] Add empty state illustration to TaskList.tsx when user has no tasks
- [X] T088 [P] Add responsive design improvements to TaskForm.tsx and TaskList.tsx for mobile devices

### Documentation & Deployment

- [X] T089 [P] Create backend/README.md with setup instructions, environment variables, and API documentation link
- [X] T090 [P] Create frontend/README.md with setup instructions, environment variables, and development workflow
- [X] T091 [P] Add API documentation endpoint to backend/main.py (FastAPI automatic docs at /docs)
- [X] T092 [P] Verify all environment variables are documented in .env.example files

---

## Dependency Graph

**User Story Completion Order**:

```
Phase 1 (Setup) → Phase 2 (Foundational)
                        ↓
                  Phase 3 (US1: Create Task) ← MVP Start
                        ↓
                  Phase 4 (US2: View Tasks) ← MVP Complete
                        ↓
                  Phase 5 (US3: Update Task) ← Enhancement
                        ↓
                  Phase 6 (US4: Delete Task) ← Full Feature
                        ↓
                  Phase 7 (Polish) ← Production Ready
```

**Critical Path**: T001-T008 → T009-T020 → T021-T037 → T038-T050

**Parallel Opportunities**:
- Phase 2: T009, T010, T011, T013-T016, T019, T020 can run in parallel
- Phase 3: T027-T028 can run in parallel with backend tasks
- Phase 4: T042-T043 can run in parallel with backend tasks
- Phase 5: T055-T056 can run in parallel with backend tasks
- Phase 6: T071 can run in parallel with backend tasks
- Phase 7: All tasks (T081-T092) can run in parallel

---

## Parallel Execution Examples

### Phase 3 (User Story 1) Parallel Execution:

**Backend Track**:
```
T021 → T022 → T023 → T024 → T025 → T026
```

**Frontend Track** (can run in parallel after T020):
```
T027 → T028 → T029 → T030 → T031 → T032 → T033
```

**Integration Track** (after both tracks complete):
```
T034 → T035 → T036 → T037
```

### Phase 4 (User Story 2) Parallel Execution:

**Backend Track**:
```
T038 → T039 → T040 → T041
```

**Frontend Track** (can run in parallel after T020):
```
T042 → T043 → T044 → T045 → T046
```

**Integration Track** (after both tracks complete):
```
T047 → T048 → T049 → T050
```

---

## MVP Scope Recommendation

**Minimum Viable Product**: Phase 1 + Phase 2 + Phase 3 + Phase 4

This delivers:
- ✅ Users can create tasks (US1)
- ✅ Users can view their tasks (US2)
- ✅ Data isolation enforced
- ✅ JWT authentication working
- ✅ Pagination implemented

**Total MVP Tasks**: 50 tasks (T001-T050)

**Post-MVP Enhancements**:
- Phase 5: Update tasks (US3) - 18 tasks
- Phase 6: Delete tasks (US4) - 12 tasks
- Phase 7: Polish - 12 tasks

---

## Task Execution Notes

1. **Sequential Dependencies**: Complete Phase 1 and Phase 2 before starting any user story phases
2. **Independent User Stories**: After Phase 2, user stories can be implemented in any order (though priority order is recommended)
3. **Parallel Execution**: Tasks marked with [P] can run in parallel with other [P] tasks in the same phase
4. **Testing**: Integration tests (T034-T037, T047-T050, etc.) must run after implementation tasks complete
5. **Environment Setup**: Ensure .env files are configured before running any backend/frontend tasks

---

## Success Criteria

**Phase 3 Complete (US1)**:
- ✅ POST /api/{user_id}/tasks endpoint working
- ✅ Task creation form functional
- ✅ Validation working (title required, length limits)
- ✅ Tasks saved to database with correct user_id

**Phase 4 Complete (US2 - MVP)**:
- ✅ GET /api/{user_id}/tasks endpoint working
- ✅ Task list displays all user's tasks
- ✅ Pagination working correctly
- ✅ Data isolation verified (users only see own tasks)

**Phase 5 Complete (US3)**:
- ✅ GET /api/{user_id}/tasks/{task_id} endpoint working
- ✅ PUT /api/{user_id}/tasks/{task_id} endpoint working
- ✅ Task edit form functional
- ✅ Partial updates working

**Phase 6 Complete (US4)**:
- ✅ DELETE /api/{user_id}/tasks/{task_id} endpoint working
- ✅ Delete button with confirmation working
- ✅ Deleted tasks removed from database and UI

**Phase 7 Complete (Production Ready)**:
- ✅ Error handling comprehensive
- ✅ UI/UX polished
- ✅ Documentation complete
- ✅ Ready for deployment
