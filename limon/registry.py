from .collector import Collector


class Registry(Collector):
    def __init__(self):
        self._collectors: list[Collector] = []

    def collect(self):
        for collector in self._collectors:
            yield from collector.collect()

    def register(self, collector: Collector):
        self._collectors.append(collector)

    def unregister(self, collector: Collector):
        try:
            self._collectors.remove(collector)
        except ValueError:
            pass


REGISTRY = Registry()
