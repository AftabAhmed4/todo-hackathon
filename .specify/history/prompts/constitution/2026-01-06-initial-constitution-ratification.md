---
id: const-20260106-001
title: initial-constitution-ratification
stage: constitution
date: 2026-01-06
surface: cli
model: claude-sonnet-4-5
feature: ""
branch: master
user: user
command: /sp.constitution
labels: [constitution, governance, initial]
links:
  spec: ""
  ticket: ""
  adr: ""
  pr: ""
files:
  - path: .specify/memory/constitution.md
    impact: created
  - path: .specify/templates/plan-template.md
    impact: updated
tests:
  - path: ""
    status: ""
---

## Prompt

You are defining the governing principles, architectural rules, and development constraints
for Phase II of a Todo Full-Stack Web Application.

PROJECT OVERVIEW
This project transforms an existing console-based Todo application into a modern, multi-user,
full-stack web application with persistent storage, authentication, and RESTful APIs.

The project MUST follow a strict spec-driven, agentic development workflow using:
Spec-Kit Plus → Claude Code → Tasks → Implementation.
No manual coding is allowed at any stage.

PRIMARY OBJECTIVES
- Implement all 5 Basic Level Todo features as a web application
- Support multiple authenticated users
- Persist data using Neon Serverless PostgreSQL
- o direct frontend-to-database access
- No hardcoded secrets
- Environment variables for all secrets and DB URLs
- Reusable, modular code structure

DATABASE PRINCIPLES
- Use SQLModel for all database interactions
- Tasks must be owned by a user (foreign key or equivalent)
- Queries must always filter by authenticated user ID
- No shared or global tSecure all API endpoints using JWT-based authentication
- Maintain strict user data isolation
- Produce production-grade, reviewable code

TECHNOLOGY CONSTRAINTS (NON-NEGOTIABLE)
Frontend:
- Next.js 16+ using App Router
- Better Auth for authentication
- JWT tokens must be issued on login

Backend:
- Python FastAPI
- SQLModel ORM
- Neon Serverless PostgreSQL database
- Stateless backend authentication using JWT

Authentication & Security:
- Better Auth must issue JWT tokens
- JWT tokens must be sent via Authorization: Bearer <token>
- Backend must verify JWT using a shared secret (BETTER_AUTH_SECRET)
- No backend session storage
- All endpoints require authentication
- All data access must be scoped to the authenticated user

API GOVERNING RULES
- REST API endpoints MUST follow the provided contract:
  GET    /api/{user_id}/tasks
  POST   /api/{user_id}/tasks
  GET    /api/{user_id}/tasks/{id}
  PUT    /api/{user_id}/tasks/{id}
  DELETE /api/{user_id}/tasks/{id}
  PATCH  /api/{user_id}/tasks/{id}/complete

- ask visibility

FRONTEND PRINCIPLES
- Responsive, modern UI
- API client must automatically attach JWT token
- Auth state must be handled entirely on frontend
- UI must reflect authenticated user's data only
- Errors and loading states must be handled gracefully

MONOREPO RULES
- Single repository
- Separate folders for frontend and backend
- Claude Code must be able to reason about both sides together
- Spec-Kit files must live at the root or dedicated /spec directory
- Clear boundaries but shared context

QUALITY & REVIEW STANDARDS
- Code must be production-grade
- No placeholder logic
- No mock authentication
- No insecure shortcuts
- Every feature must trace back to a written spec
- If a requirement is unclear, infer conservatively and document assumptions

FAILURE CONDITIONS
The implementation is considered FAILED if:
- JWT auth is missing or bypassed
- User data leaks across accounts
- API endpoints diverge from the defined contract
- Manual coding is used instead of Claude Code
- Spec-driven workflow is skipped

CORE PRINCIPLE
Correctness > Convenience
Security > Speed
Spec > Assumptions

## Response snapshot

Successfully created the Todo Full-Stack Web Application Phase II Constitution (v1.0.0) with 8 core principles:
1. Spec-Driven Agentic Development Workflow (NON-NEGOTIABLE)
2. Database Isolation & User Data Security
3. JWT-Based Stateless Authentication
4. API Contract Adherence
5. Frontend Authentication & Data Scoping
6. Monorepo Structure
7. No Hardcoded Secrets
8. Production Quality Standards

Additionally defined Technology Stack & Constraints, Development Workflow & Quality Gates, and Governance sections with versioning policy and amendment procedures.

Updated plan-template.md Constitution Check section to include all 8 required gate verifications aligned with the new constitution principles.

## Outcome

- ✅ Impact: Initial constitution ratified, establishing 8 non-negotiable principles for Phase II Todo web application
- 🧪 Tests: None (constitution definition phase)
- 📁 Files: Created .specify/memory/constitution.md, updated .specify/templates/plan-template.md
- 🔁 Next prompts: Generate feature specifications using /sp.specify, then create implementation plans using /sp.plan
- 🧠 Reflection: Constitution successfully captures all critical security, architectural, and workflow constraints. Properly balances strict non-negotiable rules with practical implementation guidance. All templates aligned.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
