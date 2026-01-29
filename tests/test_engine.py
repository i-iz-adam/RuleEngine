import pytest
import asyncio
from rule_engine.engine import RuleEngine
from rule_engine.rule import Rule
from rule_engine.event import Event

@pytest.mark.asyncio
async def test_async_rule():
    triggered = []

    async def action(e):
        await asyncio.sleep(0)
        triggered.append(e.payload["value"])

    rule = Rule(
        event_name="test",
        condition=lambda e: e.payload.get("value") == 42,
        action=action
    )

    engine = RuleEngine()
    engine.register(rule)

    event = Event(name="test", payload={"value": 42})
    await engine.emit(event)

    assert triggered == [42]
