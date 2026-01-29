from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class Event:
    """
    Immutable event object passed through the rule engine.

    Events represent *what happened*, not state.
    All stateful data must live in ContextStore.
    """
    name: str
    payload: Mapping[str, Any]
