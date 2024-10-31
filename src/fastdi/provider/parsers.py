from collections.abc import Callable
from inspect import signature
from typing import Any


def parse_class_signature(
        origin: type,
) -> tuple[Any, dict[str, Any]]:
    init_signature = signature(origin.__init__)    # type: ignore

    depends = {}
    for k, v in init_signature.parameters.items():
        if k == 'self':
            continue
        depends[k] = v.annotation

    return origin, depends


def parse_function_signature(
        factory: Callable[..., Any],
) -> tuple[Any, dict[str, Any]]:
    factory_signature = signature(factory)

    depends = {}
    for k, v in factory_signature.parameters.items():
        depends[k] = v.annotation

    return factory_signature.return_annotation, depends
