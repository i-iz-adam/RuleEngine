from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Set

from .event import Event
from .context import ContextStore


@dataclass(slots=True)
class RuleResult:
    """
    Explicit result of a rule execution.
    """
    continue_processing: bool = True
    emitted_events: list[Event] = field(default_factory=list)


class Rule(ABC):
    """
    Base class for all rules.

    Rules must be deterministic and side-effect free
    outside of ContextStore.
    """

    name: str
    priority: int = 0
    enabled: bool = True
    tags: Set[str] = set()

    def applies(self, event: Event) -> bool:
        """
        Determines whether this rule should run for the given event.
        Override for filtering logic.
        """
        return self.enabled

    @abstractmethod
    async def apply(
        self,
        event: Event,
        context: ContextStore,
    ) -> RuleResult:
        """
        Apply the rule to the event.

        Must return a RuleResult describing how execution should proceed.
        """
        raise NotImplementedError
