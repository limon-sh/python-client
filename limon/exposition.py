from .metrics import MetricType
from .registry import REGISTRY


def generate_latest() -> str:
    """Get metrics from registry in text format.

    :return: A string containing ready-to-use metrics
    """

    def build_labels(labels: dict) -> str:
        return ','.join(
            f'{key}="{str(value)}"' for key, value in labels.items()
        )

    output = []

    for metric in REGISTRY.collect():
        if metric.type == MetricType.COUNTER:
            metric_name = metric.name + '_total'
        else:
            metric_name = metric.name

        output.append(f'# HELP {metric_name} {metric.description}')
        output.append(f'# TYPE {metric_name} {metric.type}')

        for sample in metric.samples():
            sample_labels = ''

            if sample.labels:
                sample_labels = f'{{{build_labels(sample.labels)}}}'

            output.append(f'{metric_name}{sample_labels} {sample.value}')

    return '\n'.join(output)
