from typing import List
import asyncio
from rule_engine.rule import Rule
from rule_engine.event import Event

class RuleEngine:
    """Dispatches events to registered rules in deterministic order with async support."""

    def __init__(self):
        self._rules: List[Rule] = []

    def register(self, rule: Rule) -> None:
        """Register a rule."""
        self._rules.append(rule)
        # Keep rules sorted by priority (highest first)
        self._rules.sort(key=lambda r: r.priority, reverse=True)

    def unregister(self, rule: Rule) -> None:
        """Remove a rule."""
        self._rules.remove(rule)

    async def emit(self, event: Event) -> None:
        """Evaluate all matching rules and execute their actions asynchronously."""
        for rule in self._rules:
            if rule.applies(event):
                await rule.execute(event)
