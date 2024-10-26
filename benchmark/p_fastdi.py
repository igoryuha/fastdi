from fastdi import make_resolver, Provider

from classes import (
    C, CC, CCC, CCCC,
    B, BB, BBB, BBBB,
    D, DD, DDD, DDDD,
    A,
)


provider = Provider()

REQUEST_SCOPE = 'request'


@provider.provide(scope=REQUEST_SCOPE)
def a(b: B, c: C, d: D) -> A:
    return A(b, c, d)


@provider.provide(scope=REQUEST_SCOPE)
def b(bb: BB) -> B:
    return B(bb)


@provider.provide(scope=REQUEST_SCOPE)
def bb(bbb: BBB) -> BB:
    return BB(bbb)


@provider.provide(scope=REQUEST_SCOPE)
def bbb(bbbb: BBBB) -> BBB:
    return BBB(bbbb)


@provider.provide(scope=REQUEST_SCOPE)
def bbbb() -> BBBB:
    return BBBB()


@provider.provide(scope=REQUEST_SCOPE)
def c(cc: CC) -> C:
    return C(cc)


@provider.provide(scope=REQUEST_SCOPE)
def cc(ccc: CCC) -> CC:
    return CC(ccc)


@provider.provide(scope=REQUEST_SCOPE)
def ccc(cccc: CCCC) -> CCC:
    return CCC(cccc)


@provider.provide(scope=REQUEST_SCOPE)
def cccc() -> CCCC:
    return CCCC()


@provider.provide(scope=REQUEST_SCOPE)
def d(dd: DD) -> D:
    return D(dd)


@provider.provide(scope=REQUEST_SCOPE)
def dd(ddd: DDD) -> DD:
    return DD(ddd)


@provider.provide(scope=REQUEST_SCOPE)
def ddd(dddd: DDDD) -> DDD:
    return DDD(dddd)


@provider.provide(scope=REQUEST_SCOPE)
def dddd() -> DDDD:
    return DDDD()


resolver = make_resolver(provider, scope='app')
