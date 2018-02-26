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


def develope(s, level=1):
    return s.develope(level)[0]


def factorize(s):
    pass


def substitute(s, unknown='x', value=0):
    pass


def reduce(s, level=1):
    def reduce_left(s):
        if s.left.isNum():
            s = reduce_right(s)
        else:
            s.left = reduce_left(s.left)
        return s

    def reduce_right(s):
        if s.right.isNum():
            return s.value
        else:
            s.right = reduce_right(s.right)
            return s

    if level == 0:
        return s
    elif s.isNum():
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

    def develope(self, level):
        return self, level

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
        return Div(self, other, op=' / ')

    def __floordiv__(self, other):
        return Div(self, other, op=' // ')

    def __pow__(self, other):
        return Pow(self, other)

    def isAdd(self):
        return False

    def isMul(self):
        return False

    def isNum(self):
        return False


"""Litterals"""


class Litteral(Object):
    pass


class Num(Object):
    def isNum(self):
        return True


"""Operators"""


class Operator(Object):
    """Abstract class representing an operator"""

    def __init__(self, left, right, op=None):
        if isinstance(right, int):
            right = Num(right)
        if isinstance(left, int):
            left = Num(left)
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return str(self.left) + str(self.op) + str(self.right)

    @property
    def value(self):
        return Num(eval(str(self)))

    def __eq__(self, other):
        if isinstance(other, int):
            other = Num(other)
        return self.value == other.value


class Add(Operator):
    def __init__(self, left, right, op=' + '):
        super(Add, self).__init__(left, right, op)

    def isAdd(self):
        return True

    def develope(self, level):
        self.left, level = self.left.develope(level)
        self.right, level = self.right.develope(level)
        return self, level

    def __str__(self):
        if self.op == ' - ' and self.right.isAdd():
            return str(self.left) + self.op + '(' + str(self.right) + ')'
        else:
            return super().__str__()


class Mul(Operator):
    def __init__(self, left, right, op=' * '):
        super(Mul, self).__init__(left, right, op)

    def isMul(self):
        return True

    def develope(self, level):
        if level == 0:
            return self, level
        elif self.left.isNum() and self.right.isNum():
            return self, level
        elif self.left.isAdd():
            self.left.left *= self.right
            self.left.right *= self.right
            self = self.left
            return self, level-1
        elif self.right.isAdd():
            self.right.left *= self.left
            self.right.right *= self.left
            self = self.right
            return self, level-1
        else:
            self.left, level = self.left.develope(level)
            self.right, level = self.right.develope(level)
            self, level = self.develope(level)
            return self, level

    def __str__(self):
        if self.left.isAdd() and self.right.isAdd():
            return '(' + str(self.left) + ')' + self.op + \
                '(' + str(self.right) + ')'
        elif self.left.isAdd():
            return '(' + str(self.left) + ')' + self.op + str(self.right)
        elif self.right.isAdd():
            return str(self.left) + self.op + '(' + str(self.right) + ')'
        else:
            return super().__str__()


class Sub(Add):
    def __init__(self, left, right):
        super(Sub, self).__init__(left, right, op=' - ')

    def __str__(self):
        if self.right.isAdd():
            return str(self.left) + self.op + '(' + str(self.right) + ')'
        else:
            return super().__str__()


class Div(Mul):
    def __init__(self, left, right, op):
        super(Div, self).__init__(left, right, op)


class Pow(Operator):
    def __init__(self, left, right):
        super(Pow, self).__init__(left, right, op='**')


"""Equations"""


class Equation(Operator):  # Maybe Equation is just an Operator with op=' = '
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
