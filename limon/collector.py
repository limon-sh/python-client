from abc import ABC, abstractmethod
from typing import Iterable


class Collector(ABC):
    """Collector abstract class.

    The Collector class is used to collect application metrics.
    It is designed to provide easy access to the metrics and
    to facilitate the collection of multiple metrics.

    If you need to collect third-party metrics, you can create
    your own collector and register it:

    .. code-block:: python

       from limon import REGISTRY, Collector, Counter

       metric = Counter(
           'third_party', 'Number of requests to a third-party system'
       )

       class ThirdPartyCollector(Collector):
           def collect(self):
               ...
               metric.inc()
               yield metric

       REGISTRY.register(ThirdPartyCollector())
    """

    @abstractmethod
    def collect(self) -> Iterable['Metric']:
        """Get a sequence of metrics.

        :return: Iterable sequence by metrics instances
        """
        ...
