import pytest

from limon.metrics import Counter
from limon.collector import GC_COLLECTOR
from limon.registry import REGISTRY


@pytest.fixture(scope='class')
def disable_default_metrics():
    REGISTRY.unregister(GC_COLLECTOR)


@pytest.fixture(scope='function')
def counter():
    return Counter('test', 'Test', ['test'])
