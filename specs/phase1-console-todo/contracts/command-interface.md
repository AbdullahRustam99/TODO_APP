# Command Interface Contract: Phase I - Console TODO App

**Date**: 2025-12-27
**Feature**: Phase I - Console TODO App
**Version**: 1.0.0

## Overview

This document specifies the command interface contract for the Console TODO App. It defines the expected input formats, output formats, and error handling for all console commands.

## Command Format

All commands follow the format:
```
<command> [arguments...]
```

## Command Definitions

### ADD Command
**Purpose**: Add a new task
**Format**: `add <title> [- <description>]`
**Examples**:
- `add Buy groceries`
- `add Complete project - Complete the project proposal by Friday`
**Success Response**: `Task <ID> added: <title> (<status>)`
**Error Responses**:
- `Error: Title cannot be empty`
- `Error: Invalid command format`

### VIEW Command
**Purpose**: View all tasks
**Format**: `view`
**Success Response**:
```
ID | Title              | Description        | Status
1  | Buy groceries      |                    | pending
2  | Complete project   | Complete the...    | in_progress
```
**Error Responses**: None (empty list if no tasks)

### UPDATE Command
**Purpose**: Update an existing task
**Format**: `update <id> <new_title> [- <new_description>]`
**Examples**:
- `update 1 New title`
- `update 2 Updated title - New description`
**Success Response**: `Task <ID> updated`
**Error Responses**:
- `Error: Task <ID> not found`
- `Error: Invalid task ID`
- `Error: Title cannot be empty`

### DELETE Command
**Purpose**: Delete a task
**Format**: `delete <id>`
**Examples**:
- `delete 1`
**Success Response**: `Task <ID> deleted`
**Error Responses**:
- `Error: Task <ID> not found`
- `Error: Invalid task ID`

### MARK Command
**Purpose**: Mark a task with a new status
**Format**: `mark <id> <status>`
**Status Values**: `pending`, `in_progress`, `done`
**Examples**:
- `mark 1 done`
- `mark 2 in_progress`
**Success Response**: `Task <ID> marked as <status>`
**Error Responses**:
- `Error: Task <ID> not found`
- `Error: Invalid task ID`
- `Error: Invalid status value. Use: pending, in_progress, done`

### HELP Command
**Purpose**: Display help information
**Format**: `help`
**Success Response**: Help text with all available commands
**Error Responses**: None

### EXIT Command
**Purpose**: Exit the application
**Format**: `exit`
**Success Response**: `Goodbye!` (application terminates)
**Error Responses**: None

## Error Handling Contract

All error messages follow the format:
```
Error: <descriptive message>
```

The application should never crash but should always return to the command prompt after an error.

## Validation Rules

- Task IDs must be positive integers
- Task titles must not be empty or contain only whitespace
- Status values must be one of: `pending`, `in_progress`, `done`
- Commands are case-sensitive