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


def factorize(s, level=1):
    return s.factorize(level)[0]


def substitute(s, unknown='x', value=0):
    pass


def reduce(s, level=1):
    if level == 'max':
        while not s.isNum():
            s = s.reduce(level=1)[0]
        return s
    else:
        return s.reduce(level)[0]


"""General Object"""


class Object(object):

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

    def isOperator(self):
        return False

    def isAdd(self):
        return False

    def isMul(self):
        return False

    def isNum(self):
        return False

    def isZero(self):
        return False

    def isOne(self):
        return False


"""Litterals"""


class Litteral(Object):
    pass


class Num(Object):
    def __init__(self, num):
        self.num = num

    @property
    def value(self):
        return self.num

    def factorize(self, level):
        if level == 0:
            return self, 0
        for i in range(2, self.num):
            if self.num % i == 0:
                return Mul(i, self.num//i).factorize(level-1)  # .reduce(level-1)
        return self, level

    def reduce(self, level):
        return self, level

    def develope(self, level):
        return self, level

    def isNum(self):
        return True

    def isZero(self):
        return self.num == 0

    def isOne(self):
        return self.num == 1

    def __eq__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.num == other
        elif other.isNum():
            return self.value == other.value
        else:
            return False

    def __str__(self):
        return str(self.num)

    def __repr__(self):
        return str(self)  # 'Num({})'.format(self.num)


"""Operators"""


class Operator(Object):
    """Abstract class representing an operator"""

    def __init__(self, left, right, op=None):
        if isinstance(right, int) or isinstance(right, float):
            right = Num(right)
        if isinstance(left, int) or isinstance(left, float):
            left = Num(left)
        self.left = left
        self.right = right
        self.op = op

    def isOperator(self):
        return True

    def __str__(self):
        return str(self.left) + str(self.op) + str(self.right)

    def reduce(self, level):
        if level == 0:
            return self, level
        elif self.left.isNum() and self.right.isNum():
            return Num(self.value), level-1
        else:
            self.left, level = self.left.reduce(level)
            self.right, level = self.right.reduce(level)
            self, level = self.reduce(level)
            return self, level

    def __eq__(self, other):
        if not other.isOperator():
            return False
        else:
            return self.op == other.op and self.left == other.left and self.right == other.right\
                or self.op == other.op and self.left == other.right and self.right == other.left


class Add(Operator):
    def __init__(self, left, right, op=' + '):
        super(Add, self).__init__(left, right, op)

    def isAdd(self):
        return True

    @property
    def value(self):
        return self.left.value + self.right.value

    def develope(self, level):
        if level == 0:
            return self, 0
        self.left, level = self.left.develope(level)
        self.right, level = self.right.develope(level)
        return self, level

    def __str__(self):
        if self.op == ' - ' and self.right.isAdd():
            return str(self.left) + self.op + '(' + str(self.right) + ')'
        else:
            return super(Add, self).__str__()

    def __repr__(self):
        return 'Add({}, {})'.format(repr(self.left), repr(self.right))


class Mul(Operator):
    def __init__(self, left, right, op=' * '):
        super(Mul, self).__init__(left, right, op)

    def isMul(self):
        return True

    @property
    def value(self):
        return self.left.value * self.right.value

    def factorize(self, level):
        if level == 0:
            return self, 0
        self.left, level = self.left.factorize(level)
        self.right, level = self.right.factorize(level)
        return self, level

    def develope(self, level):
        if level == 0:
            return self, 0
        elif self.left.isNum() and self.right.isNum():
            return self, level
        elif self.left.isAdd():
            self.left.left *= self.right
            self.left.right *= self.right
            return self.left, level-1
        elif self.right.isAdd():
            self.right.left *= self.left
            self.right.right *= self.left
            return self.right, level-1
        else:
            self.left, level = self.left.develope(level)
            self.right, level = self.right.develope(level)
            return self.develope(level)

    def __str__(self):
        if self.left.isAdd() and self.right.isAdd():
            return '(' + str(self.left) + ')' + self.op + \
                '(' + str(self.right) + ')'
        elif self.left.isAdd():
            return '(' + str(self.left) + ')' + self.op + str(self.right)
        elif self.right.isAdd():
            return str(self.left) + self.op + '(' + str(self.right) + ')'
        else:
            return super(Mul, self).__str__()

    def __repr__(self):
        return 'Mul({}, {})'.format(repr(self.left), repr(self.right))


class Sub(Add):
    def __init__(self, left, right):
        super(Sub, self).__init__(left, right, op=' - ')

    @property
    def value(self):
        return self.left.value - self.right.value

    def __str__(self):
        if self.right.isAdd():
            return str(self.left) + self.op + '(' + str(self.right) + ')'
        else:
            return super(Sub, self).__str__()

    def __repr__(self):
        return 'Sub({}, {})'.format(repr(self.left), repr(self.right))


class Div(Mul):
    def __init__(self, left, right, op=' / '):
        super(Div, self).__init__(left, right, op)

    @property
    def value(self):
        return self.left.value / self.right.value

    def __repr__(self):
        return 'Div({}, {})'.format(repr(self.left), repr(self.right))

    # def reduce(self, level):
    #     if self.left.isNum():
    #         self.left, level = self.left.factorize(level-1)
    #     if self.right.isNum():
    #         self.right, level = self.right.factorize(level-1)
    #     if self.left.isPrime():
    #         return self, level
    #     if self.left == self.right:
    #         return Num(1), level-1


class FloorDiv(Mul):
    def __init__(self, left, right, op=' // '):
        super(FloorDiv, self).__init__(left, right, op)

    @property
    def value(self):
        return self.left.value // self.right.value


class Pow(Operator):
    def __init__(self, left, right):
        super(Pow, self).__init__(left, right, op='**')
