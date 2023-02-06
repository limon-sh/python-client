from typing import Iterable, Any

from .collector import Collector
from .registry import Registry, REGISTRY
from .sample import Sample


class MetricType:
    COUNTER = 'counter'


class Metric(Collector):
    """Metric collector class.

    Metric is a class that extends the Collector class and
    is responsible for collecting data from a specific metric.
    The class can be used to track various performance and
    other metrics data in order to gain insights into system.

    The metric must define a get method get_sample to the
    measurement sample.
    """

    type: str

    def __init__(
            self,
            name: str,
            description: str,
            labels: Iterable[str] = (),
            label_values: Iterable[str] = (),
            registry: Registry = REGISTRY
    ):
        self.name = name
        self.description = description

        self._label_names = labels
        self._label_values = label_values
        self._metrics = {}

        if not self._label_values:
            registry.register(self)

    def collect(self):
        return [self]

    def labels(self, *args: Any, **kwargs: Any) -> 'Metric':
        if kwargs:
            label_values = tuple(kwargs[label] for label in self._label_names)
        else:
            label_values = tuple(str(label) for label in args)

        if self._label_names and label_values not in self._metrics:
            self._metrics[label_values] = self.__class__(
                name=self.name,
                description=self.description,
                labels=self._label_names,
                label_values=label_values
            )

            return self._metrics[label_values]

        return self

    def samples(self) -> Iterable[Sample]:
        if self._metrics:
            for metric in self._metrics.values():
                yield from metric.get_sample()
        else:
            yield from self.get_sample()

    def get_sample(self) -> Iterable[Sample]:
        raise NotImplementedError(
            f'Method get_sample() is not implemented for {self.__class__}'
        )


class Counter(Metric):
    """Incrementing counter metric.

    Counter measure discrete events like count of http requests,
    bytes send etc. The metric has an increasing value of 1
    or the given value:

    .. code-block:: python

       from limon import Counter

       c = Counter('count', 'Documentation')
       c.inc()      # Increment by 1
       c.inc(3.14)  # Increment by given value of `3.14`
    """

    type = 'counter'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._value = 0

    def inc(self, amount: float = 1):
        """Increment counter by the given amount or default value.

        :param amount: amount for increment
        :raises ValueError: when the amount value is less than zero
        """

        if amount < 0:
            raise ValueError(
                'Counter can only be increased by positive amount'
            )

        self._value += amount

    def get_sample(self) -> Iterable[Sample]:
        return [
            Sample(
                f'{self.name}_total',
                self._value,
                dict(zip(self._label_names, self._label_values))
            )
        ]
