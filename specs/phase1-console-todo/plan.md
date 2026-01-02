# Implementation Plan: Phase I - Console TODO App (Arrow-Key Navigation)

**Branch**: `phase1` | **Date**: 2026-01-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/phase1-console-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Interactive console-based TODO application with arrow-key navigation (↑ ↓) and Enter key selection. The application provides menu-driven task management (Add, View, Update, Delete, Mark Complete) with in-memory storage using Python data structures. The interface uses visual menu selection instead of text commands.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: `curses` library for arrow-key navigation, standard library only
**Storage**: In-memory using Python data structures (no persistence)
**Testing**: pytest for unit and integration tests
**Target Platform**: Cross-platform console application (Windows, macOS, Linux)
**Project Type**: Console application
**Performance Goals**: Menu navigation responds within 100ms
**Constraints**: <200ms p95 response time, <100MB memory, console-only interface, no numeric/command-based input
**Scale/Scope**: Single-user, in-memory session, up to 1000 tasks per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-Driven Development: Implementation must follow written specifications only (Constitution: Spec-Driven Development)
- ✅ No manual coding: Implementation must be generated using Claude Code (Constitution: Spec-Driven Development)
- ✅ Python 3.13+ requirement: Application must run on specified Python version
- ✅ In-memory storage: No database or file persistence allowed (Constitution: Phase I requirements)
- ✅ Console-based: No GUI or web interface (Constitution: Phase I requirements)
- ✅ Test-first approach: TDD mandatory for all features (Constitution: Test-First principle)
- ✅ Arrow-key navigation: Must implement menu navigation using arrow keys only (Specification requirement)

## Project Structure

### Documentation (this feature)

```text
specs/phase1-console-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py              # Console application entry point
├── models/
│   └── task.py          # Task data model
├── services/
│   └── task_manager.py  # Task CRUD operations
├── cli/
│   └── menu_navigator.py # Arrow-key navigation interface
└── lib/
    └── console_interface.py # Console I/O handling

tests/
├── unit/
│   ├── test_task.py
│   └── test_task_manager.py
├── integration/
│   └── test_menu_navigation.py
└── contract/
    └── test_cli_interface.py
```

**Structure Decision**: Single console application with clear separation of concerns between data models, business logic, and user interface components. The CLI module handles arrow-key navigation specifically for the menu system.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| curses library | Arrow-key navigation requirement | Direct terminal control needed for up/down arrow support |