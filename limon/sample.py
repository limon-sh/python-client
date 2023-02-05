from typing import Optional, NamedTuple, Dict


class Sample(NamedTuple):
    """The result of measuring a metric with a specific value."""

    suffix: str
    value: float
    labels: Optional[Dict] = None
    timestamp: float = None
