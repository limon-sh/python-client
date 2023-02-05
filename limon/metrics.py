from typing import Iterable, Any

from .collector import Collector
from .registry import Registry, REGISTRY
from .sample import Sample


class Metric(Collector):
    type: str

    def __init__(
            self,
            name: str,
            documentation: str,
            labels: Iterable[str] = (),
            label_values: Iterable[str] = (),
            registry: Registry = REGISTRY
    ):
        self.name = name
        self.documentation = documentation

        self._label_names = labels
        self._label_values = label_values
        self._metrics = {label_values: self}

        if not self._label_values:
            registry.register(self)

    def collect(self):
        return [self]

    def labels(self, *args: Any, **kwargs: Any) -> 'Metric':
        if kwargs:
            label_values = tuple(kwargs[label] for label in self._label_names)
        else:
            label_values = tuple(str(label) for label in args)

        if label_values not in self._metrics:
            self._metrics[label_values] = self.__class__(
                name=self.name,
                documentation=self.documentation,
                labels=self._label_names,
                label_values=label_values
            )

        return self._metrics[label_values]

    def samples(self) -> Iterable[Sample]:
        for metric in self._metrics.values():
            yield from metric.get_sample()

    def get_sample(self) -> Iterable[Sample]:
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

    def get_sample(self) -> Iterable[Sample]:
        return [
            Sample(
                self.name,
                self._value,
                dict(zip(self._label_names, self._label_values))
            )
        ]
