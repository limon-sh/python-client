from .registry import REGISTRY


def generate_latest() -> str:
    def build_labels(labels: dict) -> str:
        return ','.join(
            f'{key}="{str(value)}"' for key, value in labels.items()
        )

    output = []

    for metric in REGISTRY.collect():
        output.append(f'# HELP {metric.name} {metric.documentation}')
        output.append(f'# TYPE {metric.name} {metric.type}')
        for sample in metric.samples():
            if sample.labels:
                output.append(
                    f'{metric.name}{{{build_labels(sample.labels)}}} {sample.value}'
                )
            else:
                output.append(
                    f'{metric.name} {sample.value}'
                )

    return '\n'.join(output)
