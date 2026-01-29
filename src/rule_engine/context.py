from collections import defaultdict
from typing import Any, Dict

class ContextStore:
    """Stores state across events for rules."""

    def __init__(self):
        # {scope: {key: value}}
        self._store: Dict[str, Dict[Any, Any]] = defaultdict(dict)

    def set(self, scope: str, key: Any, value: Any) -> None:
        self._store[scope][key] = value

    def get(self, scope: str, key: Any, default: Any = None) -> Any:
        return self._store[scope].get(key, default)

    def increment(self, scope: str, key: Any, field: str, amount: int = 1) -> int:
        obj = self._store[scope].setdefault(key, {})
        obj[field] = obj.get(field, 0) + amount
        return obj[field]
