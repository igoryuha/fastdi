from collections.abc import Callable
from inspect import isfunction, isgeneratorfunction, signature
from typing import Any, get_args

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


def build_resolving_args(depends):
    r_ = []
    for dep_key in depends:
        r_.append(f'get({dep_key})')
    return ', '.join(r_)


class Provider:

    def __init__(self):
        self.graph = {}

    def provide(self, scope: str, cache: bool = True):
        def inner(provider):
            p_signature = signature(provider)

            depends = {}
            for k, v in p_signature.parameters.items():
                depends[k] = v.annotation

            key_type = p_signature.return_annotation

            if isgeneratorfunction(provider):
                key_type, = get_args(key_type)
                body_template = GEN_TEMPLATE
            elif isfunction(provider):
                body_template = FN_TEMPLATE

            _cache = CACHE if cache else ''

            globs = {
                'origin': provider,
                'key_type': key_type,
                **depends,
            }
            body = body_template.format_map({
                'args': build_resolving_args(depends),
                'cache': _cache,
            })
            compiled = compile(body, '<string>', 'exec')
            exec(compiled, globs)
            resolve = globs['resolve']

            self.graph[key_type] = AdjacentDependencies(
                resolve=resolve,
                key_type_scope=scope,
            )
            return provider
        return inner


class AdjacentDependencies:

    def __init__(self, resolve: Callable[..., Any], key_type_scope: str):
        self.resolve = resolve
        self.key_type_scope = key_type_scope
