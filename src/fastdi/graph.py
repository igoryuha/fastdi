from inspect import signature, isgeneratorfunction, isfunction
from typing import Any, get_args, Callable


FN_TEMPLATE = """
def resolve(get, cache, exits):
    cache[key_type] = origin({args})
    return cache[key_type]
"""


GEN_TEMPLATE = """
def resolve(get, cache, exits):
    gen = origin({args})
    cache[key_type] = gen.send(None)
    exits.append(gen)
    return cache[key_type]
"""


def build_resolving_args(depends):
    r_ = []
    for dep_key in depends:
        r_.append(f'get({dep_key})')
    return ', '.join(r_)


class Provider:

    def __init__(self):
        self.graph = {}

    def provide(self, scope: str):
        def inner(provider):
            p_signature = signature(provider)

            depends = {}
            for k, v in p_signature.parameters.items():
                depends[k] = v.annotation

            key_type = p_signature.return_annotation
            
            if isgeneratorfunction(provider):
                key_type, *_ = get_args(key_type)
                body_template = GEN_TEMPLATE
            elif isfunction(provider):
                body_template = FN_TEMPLATE

            globs = {
                'origin': provider,
                'key_type': key_type,
                **depends,
            }
            body = body_template.format_map({
                'args': build_resolving_args(depends),
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