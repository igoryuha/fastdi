Фичи:
* **Скоупы**.
* **Финализация**.
* **Модульные провайдеры**.
* **Высокая скорость резолва зависимостей**.
* **Максимально минималистичный апи**. Для работы со всеми возможностями fastdi требуется импортировать всего 2 сущности.

## Примеры использования

Все зависимости fastdi, которые вам нужны это:

```python
from fastdi import make_resolver, Provider
```

Теперь создадим несколько классов, которые будем собирать:

```python
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
```

Далее нужно создать провайдер и предоставить ему фабрики с зависимостями.
Так же необходимо обязательно указать скоуп, который отвечает за контроль жизненного цика созданного объекта:

```python
from typing import Iterable


provider = Provider()

REQUEST_SCOPE = 'request'


@provider.provide(scope=REQUEST_SCOPE)
def session() -> Iterable[Session]:
    print('get session')
    yield Session()
    # здесь пишем код, ответсвенный за закрытие сессии,
    # он автоматически будет вызван после выхода из
    # соответствующего скоуа, в данном примере после
    # выхода из REQUEST_SCOPE
    print('close session')


@provider.provide(scope=REQUEST_SCOPE)
def dao() -> DAO:
    return DAO()


@provider.provide(scope=REQUEST_SCOPE)
def domain_service(dao: DAO) -> DomainService:
    return DomainService(dao=dao)


@provider.provide(scope=REQUEST_SCOPE)
def application_service(domain_service: DomainService, dao: DAO) -> ApplicationService:
    return ApplicationService(
        domain_service=domain_service,
        dao=dao,
    )

```

Остановимся немного на примере кода выше и на машинерии работы скоупов. Скоупы контролируют
жизненный цик объекта, т.е. если объект задекларирован в скоупе **request** то
сборку этого объекта можно будет запрашивать не ранее чем вы войдете в этот скуоп 
(дальнейшие пояснения в комментариях к коду):

```python
# При создании контейнера, обязательно нужно указать
# имя глобального скоупа, его часто называют application scope,
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
```

Важный момент относительно скоупов, в fastdi скоупы бесконечные, вы можете создавать сколько угодно скоупов
и определять их иерархию контекстными менеджерами, т.е. родительский скоуп определяется порядком входа
в соответствующие контексты. Имена скоупов определяются произвольными строками, вы вольны давать им любое имя:

```python
# app scope -> request scope
with resolver(scope='request') as request_resolver:
    # request scope -> interactor scope
    with request_resolver(scope='interactor') as interactor_resolver:
        # interator scope -> action scope
        with interactor_resolver(scope='action') as action_resolver:
            # и так до бесконечности, до любой вложенности скоупов,
            # которая вам необходима
            pass
```