def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


class Person:

    def __init__(self):
        self.x = 'x'

    def greet(self):
        """Return greeting to the client please"""
        return("Hello")


# print(issubclass(Person, object))
#

"""There is a binding between the orthograph and the vocabulary !!!, between the syntax and the semantics through magic dunder methods
"""
sol1 = "x = 3 - 2\nx = 1"
print(sol1)
