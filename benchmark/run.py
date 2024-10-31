import timeit

from classes import A
from p_fastdi import resolver, REQUEST_SCOPE
from p_dishka import container, Scope


print('dishka: ', timeit.timeit('with container(scope=Scope.REQUEST) as request_container: request_container.get(A)', globals=locals()))
print('fastdi: ', timeit.timeit('with resolver(scope=REQUEST_SCOPE) as request_resolver: request_resolver.get(A)', globals=locals()))
