RuleEngine Architecture
This document defines the execution model and invariants of the RuleEngine.
Execution Model
An Event is emitted into the engine
Rules are evaluated in priority order
Each rule may mutate context or stop propagation
Execution results are recorded and returned
Determinism
Rules execute sequentially
Execution order is strictly defined by priority
No rule runs concurrently for the same event
Event vs Context
Events are immutable and describe what happened.
ContextStore is mutable and represents state.
Error Handling
Errors are handled according to the engine's configured ErrorPolicy:
FAIL_FAST
CONTINUE
COLLECT
Observability
Each engine run returns execution records including timing and errors.
Scope Boundaries
The engine does not manage persistence, retries, scheduling, or external resources.