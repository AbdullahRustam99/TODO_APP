---
description: "Task list for Phase I Console TODO App with Arrow-Key Navigation"
---

# Tasks: Phase I - Console TODO App (Arrow-Key Navigation)

**Input**: Design documents from `/specs/phase1-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Test-driven development approach requested per constitution

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow the single project structure defined in plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in src/
- [ ] T002 Initialize Python 3.13 project with requirements.txt
- [ ] T003 [P] Configure linting and formatting tools (pylint, black, flake8)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create Task data model in src/models/task.py with id, title, description, completed
- [ ] T005 [P] Create TaskCollection in-memory storage in src/services/task_manager.py
- [ ] T006 [P] Setup curses-based menu navigation in src/cli/menu_navigator.py
- [ ] T007 Create console interface utilities in src/lib/console_interface.py
- [ ] T008 Configure error handling and validation in all foundational components
- [ ] T009 Setup application entry point in src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Interactive Menu Navigation (Priority: P1) 🎯 MVP

**Goal**: Implement arrow-key navigation (↑ ↓) and Enter key selection for menu options

**Independent Test**: Launch the application and navigate through menu options using arrow keys and Enter key

### Tests for User Story 1 (Test-driven approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for menu navigation in tests/contract/test_menu_navigation.py
- [ ] T011 [P] [US1] Integration test for menu selection flow in tests/integration/test_menu_flow.py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create MenuNavigator class in src/cli/menu_navigator.py
- [ ] T013 [US1] Implement arrow-key input handling in src/cli/menu_navigator.py
- [ ] T014 [US1] Implement menu display with highlighting in src/cli/menu_navigator.py
- [ ] T015 [US1] Add menu looping functionality (bottom to top, top to bottom)
- [ ] T016 [US1] Create main menu with options: Add Task, View Tasks, Update Task, Delete Task, Mark Complete, Exit
- [ ] T017 [US1] Add visual feedback for current selection
- [ ] T018 [US1] Implement menu selection execution in src/cli/menu_navigator.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management Operations (Priority: P2)

**Goal**: Implement add, view, update, delete, and mark tasks as complete using arrow-key navigation

**Independent Test**: Use the menu navigation to access each task operation and verify it works correctly

### Tests for User Story 2 (Test-driven approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T019 [P] [US2] Contract test for task operations in tests/contract/test_task_operations.py
- [ ] T020 [P] [US2] Integration test for task management flow in tests/integration/test_task_management.py

### Implementation for User Story 2

- [ ] T021 [P] [US2] Implement Add Task functionality in src/cli/menu_navigator.py
- [ ] T022 [P] [US2] Implement View Tasks functionality in src/cli/menu_navigator.py
- [ ] T023 [US2] Implement Update Task functionality in src/cli/menu_navigator.py
- [ ] T024 [US2] Implement Delete Task functionality in src/cli/menu_navigator.py
- [ ] T025 [US2] Implement Mark Task Complete/Incomplete functionality in src/cli/menu_navigator.py
- [ ] T026 [US2] Connect task operations to TaskManager service
- [ ] T027 [US2] Add task display with ID, title, and completion status (✓ Completed / ✗ Pending)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Error Handling and Input Validation (Priority: P3)

**Goal**: Handle invalid inputs gracefully and provide clear feedback to prevent application crashes

**Independent Test**: Enter invalid task IDs, empty titles, and other invalid inputs to verify proper error handling

### Tests for User Story 3 (Test-driven approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T028 [P] [US3] Contract test for error handling in tests/contract/test_error_handling.py
- [ ] T029 [P] [US3] Integration test for invalid input scenarios in tests/integration/test_error_scenarios.py

### Implementation for User Story 3

- [ ] T030 [P] [US3] Add validation for empty task titles in src/services/task_manager.py
- [ ] T031 [US3] Add validation for invalid task IDs in src/services/task_manager.py
- [ ] T032 [US3] Implement user-friendly error messages in src/lib/console_interface.py
- [ ] T033 [US3] Add input validation for all user inputs
- [ ] T034 [US3] Prevent application crashes due to invalid user input
- [ ] T035 [US3] Add confirmation prompt for task deletion
- [ ] T036 [US3] Implement graceful exit functionality in src/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T037 [P] Documentation updates in docs/
- [ ] T038 Code cleanup and refactoring
- [ ] T039 Performance optimization for menu navigation (response within 100ms)
- [ ] T040 [P] Additional unit tests in tests/unit/
- [ ] T041 Security hardening
- [ ] T042 Run quickstart.md validation

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on TaskManager service from foundational phase
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on TaskManager and menu system from other stories

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
# Launch all tests for User Story 1 together:
Task: "Contract test for menu navigation in tests/contract/test_menu_navigation.py"
Task: "Integration test for menu selection flow in tests/integration/test_menu_flow.py"

# Launch all implementation for User Story 1 together:
Task: "Create MenuNavigator class in src/cli/menu_navigator.py"
Task: "Implement arrow-key input handling in src/cli/menu_navigator.py"
Task: "Implement menu display with highlighting in src/cli/menu_navigator.py"
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