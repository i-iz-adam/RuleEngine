class RuleEngineError(Exception):
    """Base exception for RuleEngine."""

class RuleDisabledError(RuleEngineError):
    """Raised when attempting to execute a disabled rule."""
