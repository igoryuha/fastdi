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

from fastdi import Provider, make_resolver

REQUEST_SCOPE = 'request'
APP_SCOPE = 'app'

provider = Provider(scope=REQUEST_SCOPE)

provider.provide(A)
provider.provide(B)
provider.provide(BB)
provider.provide(BBB)
provider.provide(BBBB)
provider.provide(C)
provider.provide(CC)
provider.provide(CCC)
provider.provide(CCCC)
provider.provide(D)
provider.provide(DD)
provider.provide(DDD)
provider.provide(DDDD)

resolver = make_resolver(provider, scope=APP_SCOPE)
