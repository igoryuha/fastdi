from collections.abc import Callable, Generator
from inspect import isfunction, isgeneratorfunction
from typing import Any, get_args

Exits = list[Generator]
Cache = dict[Any, Any]
Get = Callable[[Any], Any]

Resolve = Callable[[Get, Cache, Exits], Any]

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


def make_args(vars_for_resolve: dict[str, Any]) -> str:
    r_ = []
    for varname in vars_for_resolve:
        r_.append(f'get({varname})')
    return ', '.join(r_)


def compile_resolve_frome_class(
        origin: type,
        vars_for_resolve: dict[str, Any],
        with_cache: bool = True,
) -> Resolve:
    return compile_resolve(
        origin=origin,
        key_type=origin,
        vars_for_resolve=vars_for_resolve,
        body_template=FN_TEMPLATE,
        with_cache=with_cache,
    )


def compile_resolve_from_function(
        factory: Callable[..., Any],
        vars_for_resolve: dict[str, Any],
        key_type: Any,
        with_cache: bool = True,
) -> Resolve:
    if isgeneratorfunction(factory):
        key_type, = get_args(key_type)
        body_template = GEN_TEMPLATE
    elif isfunction(factory):
        body_template = FN_TEMPLATE

    return compile_resolve(
        origin=factory,
        key_type=key_type,
        vars_for_resolve=vars_for_resolve,
        body_template=body_template,
        with_cache=with_cache,
    )


def compile_resolve(
        origin: Callable[..., Any],
        key_type: Any,
        vars_for_resolve: dict[str, Any],
        body_template: str,
        with_cache = True,
) -> Resolve:
    cache = CACHE if with_cache else ''
    args = make_args(vars_for_resolve)

    global_vars = {
        'origin': origin,
        'key_type': key_type,
        **vars_for_resolve,
    }
    body = body_template.format_map({
        'args': args,
        'cache': cache,
    })
    compiled = compile(body, '<string>', 'exec')
    exec(compiled, global_vars)

    return global_vars['resolve']
