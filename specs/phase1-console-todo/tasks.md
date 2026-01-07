---
description: "Task list template for feature implementation"
---

# Tasks: Phase I - Console TODO App

**Input**: Design documents from `/specs/phase1-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in src/
- [ ] T002 Initialize Python project with proper directory structure
- [ ] T003 [P] Create src/models/, src/services/, src/cli/ directories

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Create Task data model in src/models/task.py with id, title, description, status, created_at
- [ ] T005 [P] Create TaskStatus enum in src/models/task.py with pending, in_progress, done values
- [ ] T006 Create TaskManager service in src/services/task_manager.py with CRUD operations
- [ ] T007 Implement in-memory storage in TaskManager using Python dict/list
- [ ] T008 Create ConsoleInterface class in src/cli/console_interface.py for command parsing
- [ ] T009 Setup error handling and validation in all foundational components

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to add, view, and manage tasks through a console interface

**Independent Test**: Can be fully tested by adding tasks, viewing them, and confirming they persist in memory during the session.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Unit test for Task model in tests/unit/test_task.py
- [ ] T011 [P] [US1] Integration test for console flow in tests/integration/test_console_flow.py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Implement add_task functionality in src/services/task_manager.py
- [ ] T013 [P] [US1] Implement list_tasks functionality in src/services/task_manager.py
- [ ] T014 [US1] Implement command parsing for 'add' command in src/cli/console_interface.py
- [ ] T015 [US1] Implement command parsing for 'view' command in src/cli/console_interface.py
- [ ] T016 [US1] Implement command parsing for 'help' command in src/cli/console_interface.py
- [ ] T017 [US1] Add validation for task title in src/models/task.py
- [ ] T018 [US1] Add default 'pending' status for new tasks in src/services/task_manager.py
- [ ] T019 [US1] Create main.py entry point with basic command loop

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Modification (Priority: P2)

**Goal**: Allow users to update and delete tasks and mark them with different statuses

**Independent Test**: Can be tested by adding tasks, modifying them, and verifying the changes persist in memory.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T020 [P] [US2] Unit test for TaskManager update/delete operations in tests/unit/test_task_manager.py
- [ ] T021 [P] [US2] Integration test for update/delete commands in tests/integration/test_console_flow.py

### Implementation for User Story 2

- [ ] T022 [P] [US2] Implement update_task functionality in src/services/task_manager.py
- [ ] T023 [P] [US2] Implement delete_task functionality in src/services/task_manager.py
- [ ] T024 [P] [US2] Implement mark_task_status functionality in src/services/task_manager.py
- [ ] T025 [US2] Implement command parsing for 'update' command in src/cli/console_interface.py
- [ ] T026 [US2] Implement command parsing for 'delete' command in src/cli/console_interface.py
- [ ] T027 [US2] Implement command parsing for 'mark' command in src/cli/console_interface.py
- [ ] T028 [US2] Add validation for task status updates in src/models/task.py
- [ ] T029 [US2] Add validation for task ID existence in src/services/task_manager.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Application Lifecycle (Priority: P3)

**Goal**: Provide a clean way for users to exit the application and handle errors gracefully

**Independent Test**: Can be tested by starting the application and using the exit command to terminate it properly.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T030 [P] [US3] Unit test for graceful exit functionality in tests/unit/test_console_interface.py
- [ ] T031 [P] [US3] Integration test for error handling in tests/integration/test_console_flow.py

### Implementation for User Story 3

- [ ] T032 [P] [US3] Implement graceful exit functionality in src/cli/console_interface.py
- [ ] T033 [P] [US3] Implement command parsing for 'exit' command in src/cli/console_interface.py
- [ ] T034 [US3] Implement error handling for invalid commands in src/cli/console_interface.py
- [ ] T035 [US3] Add user-friendly error messages with guidance in src/cli/console_interface.py
- [ ] T036 [US3] Implement input validation for all commands in src/cli/console_interface.py
- [ ] T037 [US3] Add proper exception handling throughout the application
- [ ] T038 [US3] Implement proper cleanup on exit in src/main.py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T039 [P] Documentation updates in docs/
- [ ] T040 Code cleanup and refactoring
- [ ] T041 Performance optimization across all stories
- [ ] T042 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T043 Security hardening
- [ ] T044 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task model in tests/unit/test_task.py"
Task: "Integration test for console flow in tests/integration/test_console_flow.py"

# Launch all models for User Story 1 together:
Task: "Implement add_task functionality in src/services/task_manager.py"
Task: "Implement list_tasks functionality in src/services/task_manager.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence