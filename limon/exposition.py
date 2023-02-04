from .registry import REGISTRY


def generate_latest() -> str:
    output = []

    for metric in REGISTRY.collect():
        output.append(f'# HELP {metric.name} {metric.documentation}')
        output.append(f'# TYPE {metric.name} {metric.type}')
        output.extend(
            f'{metric.name} {sample.value}' for sample in metric.samples()
        )

    return '\n'.join(output)
