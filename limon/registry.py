from typing import Dict, Tuple

from .collector import Collector, GC_COLLECTOR


class Registry(Collector):
    """Registry of collection metrics.

    The Registry class is a utility class used to register
    collectors for metrics collection. It allows for easy
    registration and unregistration of collectors.
    """

    def __init__(self):
        self._collectors: Dict[Tuple[str, str], Collector] = {}

    def collect(self):
        for collector in self._collectors.copy().values():
            yield from collector.collect()

    def register(self, collector: Collector):
        """Registration a new collector of metrics.

        :param collector: An instance of the Collector class
        """

        collector_key = self._get_collector_key(collector)

        # Collectors within themselves can create new metrics
        # that also register themselves in the registry.
        # As a result, it turns out that metric is registered twice.
        # To avoid this need to create a collector key and check
        # that such a metric has not been registered already.
        if collector_key not in self._collectors:
            self._collectors[collector_key] = collector

    def unregister(self, collector: Collector):
        """Unregistration a collector of metrics.

        :param collector: An instance of the Collector class
        """

        self._collectors.pop(self._get_collector_key(collector), None)

    @staticmethod
    def _get_collector_key(collector) -> Tuple[str, str]:
        """Get unique name for collector.

        :param collector: An instance of the Collector class
        :return: Tuple of type and name of collector
        """

        #
        return (
            getattr(collector, 'type', Collector.__class__.__name__),
            getattr(collector, 'name', collector.__class__.__name__)
        )


REGISTRY = Registry()
REGISTRY.register(GC_COLLECTOR)
