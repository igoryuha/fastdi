from collections.abc import Callable
from inspect import isclass, isfunction
from typing import Any

from fastdi.graph import (
    AdjacentDependencies,
    build_adj_deps_from_class,
    build_adj_deps_from_factory,
)

from .parsers import (
    parse_class_signature,
    parse_function_signature,
)

Graph = dict[Any, AdjacentDependencies]


class Provider:

    def __init__(self, scope: str | None = None):
        self.graph: Graph = {}
        self.scope = scope

    def provide(
            self,
            origin: Callable[..., Any] | None = None,
            *,
            scope: str | None = None,
            cache: bool = True,
    ):
        scope = scope if scope else self.scope
        if not scope:
            raise RuntimeError

        if origin:
            if isclass(origin):
                return self._register_class(
                    origin=origin,
                    scope=scope,
                    cache=cache,
                )
            elif isfunction(origin):
                return self._register_factory(
                    provider=origin,
                    scope=scope,
                    cache=cache,
                )

        def inner(provider):
            return self._register_factory(
                provider=provider,
                scope=scope,
                cache=cache,
            )
        return inner

    def _register_class(
            self,
            origin: type,
            scope: str,
            cache: bool,
    ):
        key_type, depends = parse_class_signature(origin)

        adjacent_dependencies = build_adj_deps_from_class(
            origin=origin,
            scope=scope,
            depends=depends,
            with_cache=cache,
        )
        self.graph[key_type] = adjacent_dependencies

    def _register_factory(
            self,
            provider: Callable[..., Any],
            scope: str,
            cache: bool,
    ):
        key_type, depends = parse_function_signature(provider)

        adjacent_dependencies = build_adj_deps_from_factory(
            factory=provider,
            scope=scope,
            depends=depends,
            key_type=key_type,
            with_cache=cache,
        )
        self.graph[key_type] = adjacent_dependencies

        return provider
