class A:

    def __init__(self, x):
        self.__x = x


class B:

    def __init__(self, x):
        self.__x = x


class C(A, B):

    def __init__(self):
        self.__x = x


k = A(5)
print(k._A__x)
