from dataclasses import dataclass
from typing import Mapping, Any

@dataclass(frozen=True)
class Event:
    """Immutable event for the RuleEngine."""
    name: str
    payload: Mapping[str, Any]
