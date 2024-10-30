from __future__ import annotations

from typing import Any, Generator

from .graph import Provider, AdjacentDependencies


class Resolver:

    __slots__ = (
        "graph",
        "cache",
        "exits",
        "scope",
        "parent",
    )

    def __init__(
            self, 
            graph: dict[Any, AdjacentDependencies],
            scope: str, 
            parent: Resolver | None = None,
    ):
        self.graph = graph
        self.scope = scope
        self.parent = parent
        self.cache: dict[Any, Any] = {}
        self.exits: list[Generator] = []

    def get(self, key_type):
        if key_type in self.cache:
            return self.cache.get(key_type)

        try:
            adjacent_deps = self.graph[key_type]
        except KeyError:
            raise ValueError

        if self.scope != adjacent_deps.key_type_scope:
            try:
                return self.parent.get(key_type)
            except AttributeError:
                raise ValueError
            
        return adjacent_deps.resolve(self.get, self.cache, self.exits)
    
    def close(self):
        self.cache = {}
        for _exit in self.exits:
            try:
                _exit.send(None)
            except StopIteration:
                pass

    def __call__(self, scope: str):
        resolver = Resolver(
            graph=self.graph,
            scope=scope,
            parent=self,
        )
        return ScopeContext(resolver)


class ScopeContext:

    __slots__ = (
        "resolver",
    )

    def __init__(self, resolver):
        self.resolver = resolver

    def __enter__(self):
        return self.resolver

    def __exit__(self, exc_type, exc_value, traceback):
        self.resolver.close()


def make_resolver(*providers: Provider, scope: str) -> Resolver:
    graph = {}
    for provider in providers:
        graph.update(provider.graph)

    return Resolver(graph=graph, scope=scope)
