from classes import (
    BB,
    BBB,
    BBBB,
    CC,
    CCC,
    CCCC,
    DD,
    DDD,
    DDDD,
    A,
    B,
    C,
    D,
)
from dishka import Provider, Scope, make_container

provider = Provider(scope=Scope.REQUEST)

provider.provide(CCCC)
provider.provide(CCC)
provider.provide(CC)
provider.provide(C)
provider.provide(DDDD)
provider.provide(DDD)
provider.provide(DD)
provider.provide(D)
provider.provide(BBBB)
provider.provide(BBB)
provider.provide(BB)
provider.provide(B)
provider.provide(A)

container = make_container(provider)
