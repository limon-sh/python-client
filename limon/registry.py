from .collector import Collector


class Registry(Collector):
    """Registry of collection metrics.

    The Registry class is a utility class used to register
    collectors for metrics collection. It allows for easy
    registration and unregistration of collectors.
    """

    def __init__(self):
        self._collectors: list[Collector] = []

    def collect(self):
        for collector in self._collectors:
            yield from collector.collect()

    def register(self, collector: Collector):
        """Registration a new collector of metrics.

        :param collector: An instance of the Collector class
        """

        if collector not in self._collectors:
            self._collectors.append(collector)

    def unregister(self, collector: Collector):
        """Unregistration a collector of metrics.

        :param collector: An instance of the Collector class
        """

        try:
            self._collectors.remove(collector)
        except ValueError:
            pass


REGISTRY = Registry()
