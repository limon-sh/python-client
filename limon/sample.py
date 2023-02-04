from typing import Optional, Iterable, NamedTuple


class Sample(NamedTuple):
    name: str
    value: float
    labels: Optional[Iterable[str]] = None
    timestamp: float = None
