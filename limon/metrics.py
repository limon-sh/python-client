from collections.abc import Iterable as IterableObject
from typing import Iterable, Optional, Dict, Union

from .collector import Collector
from .registry import Registry, REGISTRY
from .sample import Sample


class Metric(Collector):
    type: str

    def __init__(
            self,
            name: str,
            documentation: str,
            labels: Optional[Union[Iterable[str], Dict]] = None,
            registry: Registry = REGISTRY
    ):
        self.name = name
        self.documentation = documentation

        if isinstance(labels, dict):
            self._labels = labels
        elif isinstance(labels, IterableObject):
            self._labels = {str(label): '' for label in labels}
        else:
            self._labels = {}

        registry.register(self)

    def collect(self):
        return [self]

    def samples(self) -> Iterable[Sample]:
        raise NotImplementedError(
            f'Samples is not implemented for {self.__class__}'
        )


class Counter(Metric):
    type = 'counter'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._value = 0

    def inc(self, amount: float = 1):
        self._value += amount

    def samples(self) -> Iterable[Sample]:
        return [Sample(self.name, self._value, self._labels)]
