from collections.abc import Callable, Generator
from inspect import isfunction, isgeneratorfunction
from typing import Any, get_args

Exits = list[Generator]
Cache = dict[Any, Any]
Get = Callable[[Any], Any]

Resolve = Callable[[Get, Cache, Exits], Any]


class AdjacentDependencies:

    __slots__ = (
        "resolve",
        "key_type_scope",
    )

    def __init__(
            self,
            resolve: Resolve,
            key_type_scope: str,
    ):
        self.resolve = resolve
        self.key_type_scope = key_type_scope


FN_TEMPLATE = """
def resolve(get, cache, exits):
    solved = origin({args})
    {cache}
    return solved
"""

GEN_TEMPLATE = """
def resolve(get, cache, exits):
    gen = origin({args})
    solved = gen.send(None)
    {cache}
    exits.append(gen)
    return solved
"""

CACHE = "cache[key_type] = solved"


def build_resolving_args(depends: dict[str, Any]) -> str:
    r_ = []
    for dep_key in depends:
        r_.append(f'get({dep_key})')
    return ', '.join(r_)


def compile_resolve_frome_class(
        origin: type,
        depends: dict[str, Any],
        with_cache: bool = True,
) -> Resolve:
    return compile_resolve_function(
        origin=origin,
        key_type=origin,
        depends=depends,
        body_template=FN_TEMPLATE,
        with_cache=with_cache,
    )


def compile_resolve_from_factory(
        factory: Callable[..., Any],
        depends: dict[str, Any],
        key_type: Any,
        with_cache: bool = True,
) -> Resolve:
    if isgeneratorfunction(factory):
        key_type, = get_args(key_type)
        body_template = GEN_TEMPLATE
    elif isfunction(factory):
        body_template = FN_TEMPLATE

    return compile_resolve_function(
        origin=factory,
        key_type=key_type,
        depends=depends,
        body_template=body_template,
        with_cache=with_cache,
    )


def compile_resolve_function(
        origin: Callable[..., Any],
        key_type: Any,
        depends: dict[str, Any],
        body_template: str,
        with_cache = True,
) -> Resolve:
    cache = CACHE if with_cache else ''
    args = build_resolving_args(depends)

    globs = {
        'origin': origin,
        'key_type': key_type,
        **depends,
    }
    body = body_template.format_map({
        'args': args,
        'cache': cache,
    })
    compiled = compile(body, '<string>', 'exec')
    exec(compiled, globs)

    return globs['resolve']


def build_adj_deps_from_class(
        origin: type,
        scope: str,
        depends: dict[str, Any],
        with_cache: bool = True,
) -> AdjacentDependencies:
    resolve = compile_resolve_frome_class(
        origin=origin,
        depends=depends,
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
    resolve = compile_resolve_from_factory(
        factory=factory,
        depends=depends,
        key_type=key_type,
        with_cache=with_cache,
    )
    return AdjacentDependencies(
        resolve=resolve,
        key_type_scope=scope,
    )
