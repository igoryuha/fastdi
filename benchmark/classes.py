class CCCC:

    def __init__(self):
        pass


class CCC:

    def __init__(self, c: CCCC):
        pass


class CC:

    def __init__(self, c: CCC):
        pass


class C:

    def __init__(self, c: CC):
        pass


class BBBB:

    def __init__(self):
        pass


class BBB:

    def __init__(self, b: BBBB):
        pass


class BB:

    def __init__(self, b: BBB):
        pass


class B:

    def __init__(self, b: BB):
        pass


class DDDD:

    def __init__(self):
        pass

    
class DDD:

    def __init__(self, d: DDDD):
        pass


class DD:

    def __init__(self, d: DDD):
        pass


class D:

    def __init__(self, d: DD):
        pass


class A:

    def __init__(self, b: B, c: C, d: D):
        pass
