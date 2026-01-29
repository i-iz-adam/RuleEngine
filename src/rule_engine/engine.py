from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, List

from .context import ContextStore
from .event import Event
from .exceptions import RuleExecutionError
from .rule import Rule, RuleResult


class ErrorPolicy(Enum):
    """
    Defines how the engine handles rule execution errors.
    """
    FAIL_FAST = auto()
    CONTINUE = auto()
    COLLECT = auto()


@dataclass(slots=True)
class RuleExecutionRecord:
    rule_name: str
    applied: bool
    duration_ms: float
    error: Exception | None = None


@dataclass(slots=True)
class EngineRunResult:
    records: List[RuleExecutionRecord]
    errors: List[Exception]


class RuleEngine:
    """
    Deterministic, sequential, async rule engine.
    """

    def __init__(
        self,
        *,
        error_policy: ErrorPolicy = ErrorPolicy.FAIL_FAST,
    ) -> None:
        self._rules: list[Rule] = []
        self._error_policy = error_policy

    def register(self, rule: Rule) -> None:
        self._rules.append(rule)
        self._rules.sort(key=lambda r: r.priority, reverse=True)

    def register_many(self, rules: Iterable[Rule]) -> None:
        for rule in rules:
            self.register(rule)

    async def emit(
        self,
        event: Event,
        context: ContextStore | None = None,
    ) -> EngineRunResult:
        """
        Emit an event through the engine.

        Execution is sequential and deterministic.
        """
        context = context or ContextStore()
        records: list[RuleExecutionRecord] = []
        errors: list[Exception] = []

        for rule in self._rules:
            if not rule.applies(event):
                records.append(
                    RuleExecutionRecord(
                        rule_name=rule.name,
                        applied=False,
                        duration_ms=0.0,
                    )
                )
                continue

            start = time.perf_counter()
            try:
                result: RuleResult = await rule.apply(event, context)
            except Exception as exc:
                record = RuleExecutionRecord(
                    rule_name=rule.name,
                    applied=True,
                    duration_ms=(time.perf_counter() - start) * 1000,
                    error=exc,
                )
                records.append(record)
                errors.append(exc)

                if self._error_policy is ErrorPolicy.FAIL_FAST:
                    raise RuleExecutionError(
                        f"Rule '{rule.name}' failed"
                    ) from exc

                if self._error_policy is ErrorPolicy.COLLECT:
                    continue

                continue

            records.append(
                RuleExecutionRecord(
                    rule_name=rule.name,
                    applied=True,
                    duration_ms=(time.perf_counter() - start) * 1000,
                )
            )

            if not result.continue_processing:
                break

        return EngineRunResult(records=records, errors=errors)
