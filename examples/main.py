from fastdi import make_resolver, Provider

from typing import Iterable


class Session:
    pass


class DAO:

    def __init__(self, session: Session):
        pass


class DomainService:

    def __init__(self, dao: DAO):
        pass


class ApplicationService:

    def __init__(self, domain_service: DomainService, dao: DAO):
        pass


provider = Provider()

REQUEST_SCOPE = 'request'


@provider.provide(scope=REQUEST_SCOPE)
def session() -> Iterable[Session]:
    print('get session')
    yield Session()
    # здесь пишем код, ответственный за закрытие сессии,
    # он автоматически будет вызван после выхода из
    # соответствующего скоупа, в данном примере после
    # выхода из REQUEST_SCOPE
    print('close session')


@provider.provide(scope=REQUEST_SCOPE)
def dao(session: Session) -> DAO:
    return DAO(session=session)


@provider.provide(scope=REQUEST_SCOPE)
def domain_service(dao: DAO) -> DomainService:
    return DomainService(dao=dao)


@provider.provide(scope=REQUEST_SCOPE)
def application_service(domain_service: DomainService, dao: DAO) -> ApplicationService:
    return ApplicationService(
        domain_service=domain_service,
        dao=dao,
    )


# При создании контейнера, обязательно нужно указать
# имя глобального скоупа, его часто называют application scoupe,
# объекты принадлежащие этому скоупу никогда не будут уничтожены.
resolver = make_resolver(provider, scope='app')

# Вход в скоуп контролируется контекстными менеджерами,
# благодаря им на момент выхода из скоупа, которому принадлежит
# объект, он будет автоматически финализирован.

# По умолчанию мы всегда находимся в глобальном скоупе,
# войдем теперь в созданный нами выше REQUEST_SCOPE
with resolver(scope=REQUEST_SCOPE) as request_resolver:
    # здесь мы можем попросить контейнер собрать объекты
    # принадлежащие этому или родительским скоупам,
    # соберем наш ApplicationService
    service = request_resolver.get(ApplicationService)
    print(service)

# после выхода из данного контекста все принадлежащие ему 
# объекты будут финализированны, к примеру если запустить
# этот код то по выходу из контекста REQUEST_SCOPE 
# вы увидите 'close session'


# app scope -> request scope
with resolver(scope='request') as request_resolver:
    # request scope -> interactor scope
    with request_resolver(scope='interactor') as interactor_resolver:
        # interator scoue -> action scope
        with interactor_resolver(scope='action') as action_resolver:
            # и так до бесконечности, до любой вложенности скоупов,
            # которая вам необходима
            pass