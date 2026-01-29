# RuleEngine

A deterministic, asynchronous, event-driven rule engine for Python.

This project provides a small but robust core for building systems that react to
events using ordered, composable rules. It is intentionally framework-agnostic
and contains no I/O, networking, or UI code.

## Design Goals

- Deterministic execution
- Explicit control flow
- Strong separation of event vs state
- Safe, inspectable failure handling
- Easy to extend without modifying core code

## Non-Goals

- No built-in persistence
- No scheduling or cron
- No concurrency inside a single event emission
- No opinionated integrations (Discord, web frameworks, etc.)

Those concerns are meant to live *outside* the engine.

## Core Concepts

### Event
An immutable description of something that happened.

### ContextStore
A mutable key-value store shared across rules during a single engine run.

### Rule
An async unit of logic that may inspect events, mutate context, and control propagation.

### RuleEngine
Coordinates rule execution in a predictable, observable way.

## Running Tests

```bash
pytest
```

or via Docker:

```bash
docker build -t rule_engine:dev .
docker run --rm rule_engine:dev
```

## Project Status

Stable core. Public API should be considered frozen until the next major version.
