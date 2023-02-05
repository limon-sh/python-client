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
        output.append(f'# HELP {metric.name} {metric.description}')
        output.append(f'# TYPE {metric.name} {metric.type}')

        for sample in metric.samples():
            metric_name = metric.name + sample.suffix

            if sample.labels:
                metric_name += f'{{{build_labels(sample.labels)}}}'

            output.append(f'{metric_name} {sample.value}')

    return '\n'.join(output)
