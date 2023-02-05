from typing import Optional, NamedTuple, Dict


class Sample(NamedTuple):
    name: str
    value: float
    labels: Optional[Dict] = None
    timestamp: float = None
