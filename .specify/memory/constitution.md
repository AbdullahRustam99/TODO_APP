<!-- Sync Impact Report:
Version change: N/A (initial version) → 1.0.0
List of modified principles: N/A (new constitution)
Added sections: All principles and sections (new constitution)
Removed sections: N/A
Templates requiring updates: N/A (initial constitution)
Follow-up TODOs: None
-->
# AI TODO APP Constitution

## Core Principles

### Spec-Driven Development
All implementation must be generated using Claude Code based only on written specifications. Manual coding is not allowed. The project must follow Spec-Driven Development methodology across all five phases.

### Phase-Based Evolution
The application must evolve iteratively across five phases (Console → Web → AI → Local K8s → Cloud) where each phase extends the previous one without breaking existing behavior.

### Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced for all features across all phases.

### Architecture-First Design
Every feature must be designed with clear system architecture before implementation. All architectural decisions must be documented and follow cloud-native patterns.

### AI-Native Integration
In Phase III and beyond, AI capabilities must be integrated as first-class features using OpenAI ChatKit and Agents SDK. AI must translate user intent into deterministic system actions within defined capabilities.

### Cloud-Native Deployment
In Phases IV and V, the system must follow cloud-native deployment patterns using Docker, Kubernetes, and event-driven architecture with Kafka and Dapr.

## Technology Stack Requirements
Phase I: Python in-memory data structures; Phase II: Next.js frontend, FastAPI backend, SQLModel with Neon Serverless Postgres; Phase III: OpenAI ChatKit and Agents SDK; Phase IV: Docker, Minikube, Helm, kubectl-ai, kagent; Phase V: DigitalOcean Kubernetes (DOKS), Kafka, Dapr.

## Development Workflow
Features developed iteratively following the five phases. Each phase must maintain backward compatibility. Code reviews must verify compliance with spec-driven development. All changes must reference written specifications.

## Governance
This constitution supersedes all other practices. All implementation must follow written specifications only. Amendments require documentation and approval. All PRs/reviews must verify compliance with spec-driven development principles. The constitution must be updated when adding new phases or changing fundamental project requirements.

**Version**: 1.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27