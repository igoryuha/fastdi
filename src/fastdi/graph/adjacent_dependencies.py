from .compilation import Resolve


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
