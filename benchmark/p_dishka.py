from dishka import make_container, Scope, Provider


from classes import (
    C, CC, CCC, CCCC,
    B, BB, BBB, BBBB,
    D, DD, DDD, DDDD,
    A,
)


provider = Provider(scope=Scope.APP)
provider.provide(CCCC, scope=Scope.REQUEST)
provider.provide(CCC, scope=Scope.REQUEST)
provider.provide(CC, scope=Scope.REQUEST)
provider.provide(C, scope=Scope.REQUEST)
provider.provide(DDDD, scope=Scope.REQUEST)
provider.provide(DDD, scope=Scope.REQUEST)
provider.provide(DD, scope=Scope.REQUEST)
provider.provide(D, scope=Scope.REQUEST)
provider.provide(BBBB, scope=Scope.REQUEST)
provider.provide(BBB, scope=Scope.REQUEST)
provider.provide(BB, scope=Scope.REQUEST)
provider.provide(B, scope=Scope.REQUEST)
provider.provide(A, scope=Scope.REQUEST)

container = make_container(provider)
