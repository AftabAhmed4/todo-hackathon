---

description: "Task list for Landing Page + Authentication implementation"
---

# Tasks: Landing Page + Authentication

**Input**: Design documents from `/specs/002-landing-auth/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - not included in this task list as they were not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/`
- Paths shown below follow monorepo structure with separate frontend and backend folders

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend project structure with main.py, models.py, routes/, db.py, auth.py, schemas.py
- [x] T002 [P] Create frontend project structure with app/, components/, lib/ directories
- [x] T003 [P] Install backend dependencies: fastapi, uvicorn, sqlmodel, pydantic, python-jose[cryptography], passlib[bcrypt], python-multipart, psycopg2-binary
- [x] T004 [P] Install frontend dependencies: next@16, react@18, typescript, tailwindcss, and configure tailwind.config.js
- [x] T005 [P] Create backend/.env file with DATABASE_URL and BETTER_AUTH_SECRET placeholders
- [x] T006 [P] Create frontend/.env.local file with NEXT_PUBLIC_API_URL placeholder
- [x] T007 [P] Create .env.example files in both backend/ and frontend/ with documented variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create User model with SQLModel in backend/models.py (id, email, password_hash, created_at, updated_at)
- [x] T009 Setup database connection and session management in backend/db.py with Neon PostgreSQL
- [x] T010 [P] Create JWT utility functions in backend/auth.py (create_access_token, verify_token, get_current_user dependency)
- [x] T011 [P] Create password hashing utilities in backend/auth.py using passlib with bcrypt
- [x] T012 [P] Create Pydantic request/response schemas in backend/schemas.py (SignupRequest, SigninRequest, AuthResponse, UserPublic)
- [x] T013 [P] Configure CORS middleware in backend/main.py to allow frontend origin with credentials
- [x] T014 [P] Create API client wrapper in frontend/lib/api.ts with automatic JWT token attachment
- [x] T015 [P] Create auth context and hooks in frontend/lib/auth.ts (AuthProvider, useAuth hook)
- [x] T016 [P] Create TypeScript type definitions in frontend/lib/types.ts (User, AuthResponse, ApiError)
- [x] T017 Create root layout in frontend/app/layout.tsx with AuthProvider wrapper and Tailwind CSS imports
- [x] T018 [P] Create reusable Header component in frontend/components/Header.tsx with navigation links
- [x] T019 [P] Create reusable Footer component in frontend/components/Footer.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - New User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts with email/password credentials, receive JWT tokens, and access the application

**Independent Test**: Navigate to /signup, enter valid credentials (email: test@example.com, password: TestPass123), submit form, verify account created, JWT token received, and redirect to /tasks

### Implementation for User Story 1

- [x] T020 [P] [US1] Create signup route handler in backend/routes/auth.py with POST /api/auth/signup endpoint
- [x] T021 [US1] Implement signup logic in backend/routes/auth.py: validate email/password, check duplicate email, hash password, create user, issue JWT token
- [x] T022 [US1] Add error handling in signup endpoint for duplicate email (400), invalid format (400), database errors (500)
- [x] T023 [P] [US1] Create signup page in frontend/app/signup/page.tsx with form for email and password
- [x] T024 [US1] Implement signup form validation in frontend/app/signup/page.tsx (email format, password requirements: 8+ chars, uppercase, lowercase, number)
- [x] T025 [US1] Connect signup form to backend API in frontend/app/signup/page.tsx, handle success (store token, redirect to /tasks) and errors (display messages)
- [x] T026 [P] [US1] Create reusable AuthForm component in frontend/components/AuthForm.tsx for email/password input with validation
- [x] T027 [US1] Style signup page with Tailwind CSS: responsive layout, clear labels, error messages, submit button
- [x] T028 [US1] Add client-side password strength indicator in signup form showing requirements (uppercase, lowercase, number, length)
- [x] T029 [US1] Implement JWT token storage in httpOnly cookie on successful signup (backend sets cookie in response)
- [x] T030 [US1] Add redirect logic in frontend: authenticated users visiting /signup should redirect to /tasks

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can create accounts and receive authentication tokens.

---

## Phase 4: User Story 2 - Existing User Login (Priority: P2)

**Goal**: Enable existing users to authenticate with email/password, receive JWT tokens, and access their data

**Independent Test**: Create a user account via signup, navigate to /signin, enter correct credentials, submit form, verify authentication succeeds, JWT token received, and redirect to /tasks

### Implementation for User Story 2

- [x] T031 [P] [US2] Create signin route handler in backend/routes/auth.py with POST /api/auth/signin endpoint
- [x] T032 [US2] Implement signin logic in backend/routes/auth.py: lookup user by email, verify password with bcrypt, issue JWT token
- [x] T033 [US2] Add error handling in signin endpoint with generic error message "Invalid email or password" (401) for security
- [x] T034 [P] [US2] Create signin page in frontend/app/signin/page.tsx with form for email and password
- [x] T035 [US2] Implement signin form validation in frontend/app/signin/page.tsx (email format, password not empty)
- [x] T036 [US2] Connect signin form to backend API in frontend/app/signin/page.tsx, handle success (store token, redirect to /tasks) and errors (display generic message)
- [x] T037 [US2] Reuse AuthForm component in signin page for consistent UI
- [x] T038 [US2] Style signin page with Tailwind CSS: responsive layout, clear labels, error messages, submit button, link to signup
- [x] T039 [US2] Implement JWT token storage in httpOnly cookie on successful signin (backend sets cookie in response)
- [x] T040 [US2] Add redirect logic in frontend: authenticated users visiting /signin should redirect to /tasks
- [x] T041 [US2] Create AuthGuard component in frontend/components/AuthGuard.tsx to protect routes (redirect unauthenticated users to /signin)
- [x] T042 [US2] Add logout functionality in auth context (clear token, redirect to landing page)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can create accounts and sign in to existing accounts.

---

## Phase 5: User Story 3 - Landing Page Information (Priority: P3)

**Goal**: Provide visitors with information about the application and clear calls-to-action for signup and signin

**Independent Test**: Navigate to root URL (/), verify landing page displays application description, features, benefits, prominent "Sign Up" button, and "Sign In" link

### Implementation for User Story 3

- [x] T043 [P] [US3] Create landing page in frontend/app/page.tsx with hero section, features section, and CTA buttons
- [x] T044 [US3] Add application description and value proposition to landing page (what the app does, why use it)
- [x] T045 [US3] Create features section highlighting key capabilities: multi-user support, secure authentication, data privacy
- [x] T046 [US3] Add prominent "Sign Up" button linking to /signup with eye-catching styling
- [x] T047 [US3] Add "Sign In" link for existing users linking to /signin
- [x] T048 [US3] Style landing page with Tailwind CSS: modern design, responsive layout (mobile-first), clear typography
- [x] T049 [US3] Add responsive navigation in Header component with conditional rendering (show signup/signin for unauthenticated, show dashboard link for authenticated)
- [x] T050 [US3] Optimize landing page for mobile devices: ensure all content readable at 320px width, touch-friendly buttons
- [x] T051 [US3] Add security and privacy messaging to landing page (JWT authentication, user data isolation, no data sharing)
- [x] T052 [US3] Implement redirect logic: authenticated users visiting landing page (/) should see option to go to /tasks

**Checkpoint**: All user stories should now be independently functional. Visitors can learn about the app, sign up, and sign in.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T053 [P] Add loading states to all forms (signup, signin) with spinner or skeleton during API calls
- [x] T054 [P] Add success toast notifications for successful signup and signin
- [x] T055 [P] Implement comprehensive error handling across all API calls with user-friendly messages
- [x] T056 [P] Add form field focus management and keyboard navigation (Tab, Enter to submit)
- [x] T057 [P] Ensure all error messages are accessible (ARIA labels, screen reader friendly)
- [x] T058 [P] Add password visibility toggle (show/hide password) in AuthForm component
- [x] T059 [P] Optimize API response times: add database connection pooling, optimize queries
- [x] T060 [P] Add request/response logging in backend for debugging and monitoring
- [x] T061 [P] Create placeholder /tasks page in frontend/app/tasks/page.tsx (protected route for future feature)
- [x] T062 [P] Add environment variable validation on backend startup (check DATABASE_URL, BETTER_AUTH_SECRET are set)
- [x] T063 [P] Add environment variable validation on frontend build (check NEXT_PUBLIC_API_URL is set)
- [x] T064 [P] Update README.md with setup instructions, environment variables, and running commands
- [ ] T065 [P] Test all authentication flows end-to-end: signup → signin → protected route access
- [x] T066 [P] Verify JWT token expiration handling: expired tokens redirect to signin with message
- [ ] T067 [P] Test responsive design on multiple screen sizes (320px, 768px, 1024px, 1920px)
- [ ] T068 [P] Validate constitution compliance: JWT auth working, user isolation ready, no hardcoded secrets, production quality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - No dependencies on other stories (independent)
  - User Story 3 (P3): Can start after Foundational - No dependencies on other stories (independent)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 (can be tested separately)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2 (can be tested separately)

### Within Each User Story

- Backend routes before frontend pages (need API endpoints to call)
- Form validation before API integration
- Core implementation before styling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002-T007)
- All Foundational tasks marked [P] can run in parallel within Phase 2 (T010-T019)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Within each user story, tasks marked [P] can run in parallel
- All Polish tasks marked [P] can run in parallel (T053-T068)

---

## Parallel Example: User Story 1

```bash
# Launch backend and frontend tasks for User Story 1 together:
Task: "Create signup route handler in backend/routes/auth.py" (T020)
Task: "Create signup page in frontend/app/signup/page.tsx" (T023)
Task: "Create reusable AuthForm component" (T026)

# These can run in parallel because they touch different files
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T019) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T020-T030)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Navigate to /signup
   - Enter valid credentials
   - Verify account created
   - Verify JWT token received
   - Verify redirect to /tasks
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (New User Registration) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Existing User Login) → Test independently → Deploy/Demo
4. Add User Story 3 (Landing Page) → Test independently → Deploy/Demo
5. Add Polish (Phase 6) → Final testing → Production deployment

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T019)
2. Once Foundational is done:
   - Developer A: User Story 1 (T020-T030)
   - Developer B: User Story 2 (T031-T042)
   - Developer C: User Story 3 (T043-T052)
3. Stories complete and integrate independently
4. Team completes Polish together (T053-T068)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are OPTIONAL - not included as they were not requested in spec
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 68
- **Phase 1 (Setup)**: 7 tasks
- **Phase 2 (Foundational)**: 12 tasks (BLOCKING)
- **Phase 3 (User Story 1 - P1)**: 11 tasks
- **Phase 4 (User Story 2 - P2)**: 12 tasks
- **Phase 5 (User Story 3 - P3)**: 10 tasks
- **Phase 6 (Polish)**: 16 tasks

**Parallel Opportunities**: 42 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phases 1-3 (30 tasks) deliver User Story 1 (New User Registration)

**Independent Test Criteria**:
- **US1**: Navigate to /signup, create account, verify JWT token, redirect to /tasks
- **US2**: Navigate to /signin, authenticate, verify JWT token, redirect to /tasks
- **US3**: Navigate to /, verify landing page content, CTAs work

**Constitution Compliance**: All tasks align with JWT authentication, user data isolation, no hardcoded secrets, and production quality requirements.
