#
# def solve(eq):
#         # 0123456789
#     # eq: 2x + 3 = 0
#     sol = ''
#     eq = list(eq)
#     if eq[3] == '+':
#         eq[9] = '-' + eq[5]
#     elif eq[3] == '-':
#         eq[9] = ' ' + eq[5]
#     eq[5] = ''
#     eq[3] = eq[4] = eq[6] = ''
#     sol = sol + ''.join(eq)
#     eq = list(sol)
#     # eq: '2x = -3'
#     eq[6] = eq[6] + '/' + eq[0]
#     eq[0] = ''
#     sol = sol + '\n' + ''.join(eq)
#     return sol


def develope(s):
    pass


def factorize(s):
    pass


def substitute(s, unknown='x', value=0):
    pass


def reduce(s, level=1):
    def reduce_left(s):
        if isinstance(s.left, Number):
            s = reduce_right(s)
        else:
            s.left = reduce_left(s.left)
        return s

    def reduce_right(s):
        if isinstance(s.right, Number):
            return s.value
        else:
            s.right = reduce_right(s.right)
            return s

    if level == 0:
        return s
    elif isinstance(s, Number):
        s = s.value
    else:
        s = reduce_left(s)
    return reduce(s, level-1)


"""General Object"""


class Object(object):
    def __init__(self, obj):
        self.obj = obj

    @property
    def value(self):
        return self

    def __eq__(self, other):
        return self.obj == other.obj

    def __str__(self):
        return str(self.obj)

    def __add__(self, other):
        return Add(self, other)

    def __sub__(self, other):
        return Sub(self, other)

    def __mul__(self, other):
        return Mul(self, other)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Number(other)
        return Div(self, other)

    def __floordiv__(self, other):
        if isinstance(other, int):
            other = Number(other)
        return Div(self, other, op=' // ')


"""Litterals"""


class Litteral(Object):
    pass


class Number(Object):
    pass


"""Operations"""


class Operation(Object):
    """Abstract class reprenting an operator"""

    def __init__(self, left, right, op=None):
        if isinstance(right, int):
            right = Number(right)
        if isinstance(left, int):
            left = Number(left)
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return str(self.left) + str(self.op) + str(self.right)

    @property
    def value(self):
        return Number(eval(str(self)))

    def __eq__(self, other):
        if isinstance(other, int):
            other = Number(other)
        return str(self.left) == str(other.left) and \
            str(self.right) == str(other.right)


class Add(Operation):
    def __init__(self, left, right):
        super(Add, self).__init__(left, right, op=' + ')


class Mul(Operation):
    def __init__(self, left, right):
        super(Mul, self).__init__(left, right, op=' * ')

    def __str__(self):
        if isinstance(self.left, Add) and isinstance(self.right, Add):
            return '(' + str(self.left) + ')' + self.op + \
                '(' + str(self.right) + ')'
        elif isinstance(self.left, Add):
            return '(' + str(self.left) + ')' + self.op + str(self.right)
        elif isinstance(self.right, Add):
            return str(self.left) + self.op + '(' + str(self.right) + ')'
        else:
            return super().__str__()


class Sub(Operation):
    def __init__(self, left, right):
        super(Sub, self).__init__(left, right, op=' - ')

    def __str__(self):
        if isinstance(self.right, Add):
            return str(self.left) + self.op + '(' + str(self.right) + ')'
        else:
            return super().__str__()


class Div(Operation):
    def __init__(self, left, right):
        super(Div, self).__init__(left, right, op=' / ')

    def __str__(self):
        if isinstance(self.left, Add) and isinstance(self.right, Add):
            return '(' + str(self.left) + ')' + self.op + \
                '(' + str(self.right) + ')'
        elif isinstance(self.left, Add):
            return '(' + str(self.left) + ')' + self.op + str(self.right)
        elif isinstance(self.right, Add):
            return str(self.left) + self.op + '(' + str(self.right) + ')'
        else:
            return super().__str__()


"""Equations"""


class Equation(Operation):  # Maybe Equation is just an Operation with op=' = '
    def __init__(self, left, right):
        super(Equation, self).__init__(left, right, op=' = ')

    @property
    def value(self):
        return self.left == self.right


class BasicEquation(Equation):
    """Represents a basic equation: x = b"""

    def __init__(self, left, right):
        super(BasicEquation, self).__init__()


class TermEquation(Equation):
    """Represents Equation x + a = b
    """

    def __init__(self, left, right):
        super(TermEquation, self).__init__(left, right)
