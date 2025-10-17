# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a news application project (my-news) currently in initial setup phase. The project follows a structured development approach with automatic documentation and quality management.

## Development Philosophy

This project uses a "Claude Vibe Coding" methodology defined in `DEV_GUIDE.md`, which emphasizes:

1. **Single Responsibility Principle**: One file = one clear role
2. **High Cohesion, Low Coupling**: Related features together, independent features separated
3. **Reusability First**: Extract common logic immediately
4. **Clear Naming**: File/function names express their role
5. **Automatic Documentation**: Real-time updates to structure and dependency docs

## Project Documentation Structure

The project maintains three auto-managed documentation files:

### STRUCTURE.md
- Project folder structure and file hierarchy
- Each file's role and responsibilities
- Export/import dependencies
- Code structure quality checks

### DEPENDENCIES.md
- Mermaid diagrams showing file dependencies
- External library usage (production and dev dependencies)
- Circular dependency detection
- Dependency complexity assessment

### CHANGELOG.md
- Development checkpoints (auto-triggered after 5+ file changes or major features)
- Completed features and file changes
- Project statistics and quality metrics
- Improvement suggestions
- Next steps

## Automatic Workflows

### Real-time Updates
- **File creation/modification**: Auto-update STRUCTURE.md
- **Import/export changes**: Auto-update DEPENDENCIES.md with Mermaid diagrams
- **Code quality issues**: Immediate detection and suggestions

### Checkpoint Triggers
Automatically create CHANGELOG.md entries when:
- 5+ files changed
- New domain/module added
- Major feature completed
- User explicitly requests

### Quality Checks
Automatically detect:
- Single responsibility violations
- Reusable logic opportunities
- Code duplication
- Circular dependencies
- Unnecessary coupling

## Code Organization Guidelines

### When to Split Files

**Must Split:**
- Different domains/features mixed in one file
- Reusable logic tied to specific file
- File role cannot be described in one sentence

**Consider Splitting:**
- File exceeds 500 lines with readability issues
- Multiple independently testable units
- Unrelated types/constants grouped together

**Don't Split:**
- Tightly coupled logic
- Splitting increases complexity
- Small helpers used in one place only

## Configuration

The project uses `.clauderc` to load the DEV_GUIDE.md as the system prompt, ensuring all Claude Code interactions follow the established development patterns.
