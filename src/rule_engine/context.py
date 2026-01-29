from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any


class ContextStore(MutableMapping[str, Any]):
    """
    Mutable key-value store shared across rules during execution.

    This represents system state, not the event itself.
    """

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def clear(self) -> None:
        self._data.clear()
