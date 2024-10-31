from collections.abc import Callable
from typing import Any

from .adjacent_dependencies import AdjacentDependencies
from .compilation import (
    compile_resolve_from_function,
    compile_resolve_frome_class,
)


def build_adj_deps_from_class(
        origin: type,
        scope: str,
        depends: dict[str, Any],
        with_cache: bool = True,
) -> AdjacentDependencies:
    resolve = compile_resolve_frome_class(
        origin=origin,
        vars_for_resolve=depends,
        with_cache=with_cache,
    )
    return AdjacentDependencies(
        resolve=resolve,
        key_type_scope=scope,
    )


def build_adj_deps_from_factory(
        factory: Callable[..., Any],
        scope: str,
        depends: dict[str, Any],
        key_type: Any,
        with_cache: bool = True,
) -> AdjacentDependencies:
    resolve = compile_resolve_from_function(
        factory=factory,
        vars_for_resolve=depends,
        key_type=key_type,
        with_cache=with_cache,
    )
    return AdjacentDependencies(
        resolve=resolve,
        key_type_scope=scope,
    )
