import pytest

from limon.metrics import MetricType, Counter
from limon.exposition import generate_latest
from limon.sample import Sample


@pytest.mark.usefixtures('disable_default_metrics')
class TestCounter:
    def test_metric_type(self):
        assert Counter.type == MetricType.COUNTER

    def test_initial_value(self, counter):
        assert counter._value == 0

    def test_inc_by_negative_amount(self, counter):
        with pytest.raises(ValueError):
            counter.inc(-1)

    def test_inc_by_positive_amount(self, counter):
        counter.inc(1)
        assert counter._value == 1

    def test_get_sample(self, counter):
        assert counter.get_sample() == [
            Sample(
                f'{counter.name}_total',
                counter._value,
                dict(zip(counter._label_names, counter._label_values))
            )
        ]

    def test_generate_latest(self, counter):
        assert generate_latest() == \
            f'# HELP {counter.name}_total {counter.description}\n' \
            f'# TYPE {counter.name}_total {counter.type}\n' \
            f'{counter.name}_total {counter._value}'
