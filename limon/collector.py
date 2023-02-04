from typing import Iterable


class Collector:
    def collect(self) -> Iterable['Metric']:
        raise NotImplementedError('Collector is not implemented')
