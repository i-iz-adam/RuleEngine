from __future__ import annotations
from typing import Callable, Any
from rule_engine.event import Event
from rule_engine.exceptions import RuleDisabledError

class Rule:
    """Represents a conditional action in the engine."""

    def __init__(
        self,
        event_name: str,
        condition: Callable[[Event], bool],
        action: Callable[[Event], Any],
        priority: int = 0,
        enabled: bool = True
    ):
        self.event_name = event_name
        self.condition = condition
        self.action = action
        self.priority = priority
        self.enabled = enabled

    def applies(self, event: Event) -> bool:
        return self.enabled and self.event_name == event.name and self.condition(event)

    async def execute(self, event: Event) -> None:
        if not self.enabled:
            raise RuleDisabledError(f"Rule for {self.event_name} is disabled")
        result = self.action(event)
        if callable(getattr(result, "__await__", None)):
            await result
