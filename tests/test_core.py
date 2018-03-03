import unittest

from context import Num, Add, Mul, Div, reduce, develope, factorize


class TestObject(unittest.TestCase):
    def setUp(self):
        pass

    def test_isNum(self):
        self.assertTrue(Num(3).isNum())
        self.assertFalse(Add(3, 2).isNum())
        self.assertFalse(Mul(3, 4).isNum())

    def test_isZero(self):
        self.assertTrue(Num(0).isZero())
        self.assertFalse(Num(3).isZero())
        self.assertFalse(Add(0, 0).isZero())

    def test_isOne(self):
        self.assertTrue(Num(1).isOne())
        self.assertFalse(Num(3).isOne())
        self.assertFalse(Mul(1, 1).isOne())


class TestNum(unittest.TestCase):
    def setUp(self):
        self.num1 = Num(2)
        self.num2 = Num(3)
        self.add = Add(2, 3)
        self.mul = Mul(3, 5)

    def test_value(self):
        self.assertEqual(self.num1.value, 2)
        self.assertEqual(self.num2.value, 3)

    def test_str(self):
        self.assertEqual(str(self.num1), '2')

    def test_repr(self):
        self.assertEqual(repr(Num(2)), '2')
        self.assertEqual(repr(Num(5)), '5')

    def test_eq(self):
        self.assertTrue(Num(2) == self.num1)
        self.assertFalse(Num(2) == self.num2)
        self.assertTrue(Num(4) == 4)

    def test_add(self):
        self.assertEqual(Num(2) + self.num1, Add(2, 2))
        self.assertEqual(Num(2) + self.add, Add(2, Add(2, 3)))

    def test_sub(self):
        pass

    def test_mul(self):
        pass

    def test_truediv(self):
        pass

    def test_floordiv(self):
        pass


class TestMul(unittest.TestCase):

    def test_(self):
        self.assertEqual(Mul(2, 3), Mul(3, 2))
        self.assertEqual(Mul(2, Div(4, 2)), Mul(Div(4, 2), 2))

    def test_value(self):
        self.assertEqual(Mul(2, 3).value, 6)
        self.assertEqual(Mul(-2, 4).value, -8)

    def test_str(self):
        self.assertEqual(str(Mul(2, 3)), '2 * 3')
        self.assertEqual(str(Mul(Num(2), Mul(2, 3))), '2 * 2 * 3')
        self.assertEqual(str(Mul(Mul(2, 3), Num(4))), '2 * 3 * 4')
        self.assertEqual(str(Mul(Mul(2, 3), Mul(3, 4))), '2 * 3 * 3 * 4')
        self.assertEqual(str(Mul(Num(3), Mul(2, 3))), '3 * 2 * 3')
        self.assertEqual(str(Mul(Num(3), Add(2, 3))), '3 * (2 + 3)')
        self.assertEqual(str(Mul(Add(2, 3), Num(3))), '(2 + 3) * 3')
        self.assertEqual(str(Mul(Add(2, 3), Add(3, 4))), '(2 + 3) * (3 + 4)')

    def test_repr(self):
        self.assertEqual(repr(Mul(2, 3)), 'Mul(2, 3)')
        self.assertEqual(repr(Mul(Add(2, 3), Num(4))), 'Mul(Add(2, 3), 4)')

    def test_eq(self):
        self.assertTrue(Mul(2, 3) == Mul(2, 3))
        self.assertTrue(Mul(2, 3) == Mul(3, 2))
        self.assertTrue(Mul(2, Add(2, 3)) == Mul(2, Add(2, 3)))
        self.assertTrue(Mul(2, Add(2, 3)) == Mul(Add(2, 3), 2))
        self.assertFalse(Mul(2, 3) == Num(3))
        self.assertFalse(Mul(2, 3) == Mul(2, 5))
        self.assertFalse(Mul(2, 3) == Add(2, 3))
        self.assertTrue(Num(2)*Num(2)*Num(3) == Num(2)*Num(2)*Num(3))

    def test_add(self):
        self.assertEqual(Mul(2, 3) * Num(6), Mul(Mul(2, 3), Num(6)))
        self.assertEqual(Mul(2, 3) * Mul(5, 6), Mul(Mul(2, 3), Mul(5, 6)))

    def test_sub(self):
        pass


class TestAdd(unittest.TestCase):
    def setUp(self):
        self.num = Num(2)
        self.add = Add(2, 3)
        self.mul = Mul(3, 4)

    def test_value(self):
        self.assertEqual(Add(2, 3).value, 5)
        self.assertEqual(Add(-2, 5).value, 3)

    def test_str(self):
        self.assertEqual(str(Add(2, 3)), '2 + 3')
        self.assertEqual(str(Add(Num(2), Add(2, 3))), '2 + 2 + 3')
        self.assertEqual(str(Add(Add(2, 3), Num(4))), '2 + 3 + 4')
        self.assertEqual(str(Add(Add(2, 3), Add(3, 4))), '2 + 3 + 3 + 4')
        self.assertEqual(str(Add(Num(3), Mul(2, 3))), '3 + 2 * 3')

    def test_eq(self):
        self.assertEqual(Add(2, 3), Add(2, 3))
        self.assertEqual(Add(2, 3), Add(3, 2))
        self.assertEqual(Add(2, Mul(2, 3)), Add(Mul(2, 3), 2))

    def test_add(self):
        self.assertEqual(Add(2, 3) + Num(6), Add(Add(2, 3), Num(6)))
        self.assertEqual(Add(2, 3) + Add(5, 6), Add(Add(2, 3), Add(5, 6)))

    def test_sub(self):
        pass


class TestReduce(unittest.TestCase):
    def setUp(self):
        self.one = Num(1)
        self.zero = Num(0)

    def test_reduce(self):
        self.assertEqual(reduce(Num(4)), Num(4))
        self.assertEqual(reduce(Num(2) + Num(3)), Num(5))
        self.assertEqual(reduce(Num(2) * Num(3)), Num(6))
        self.assertEqual(reduce(Num(2) * Num(3) + Num(4), level=4), Num(10))
        self.assertEqual(reduce(self.one * 2 + 3), Num(2) + Num(3))
        self.assertEqual(reduce(self.one * 2 * -1, level=2), Num(-2))
        self.assertEqual(reduce(Num(2)*Num(3) + Num(3) + Num(4)), Num(6) + Num(3) + Num(4))
        self.assertEqual(reduce(Num(2)*Num(3) + Num(3) + Num(4)), Num(6) + Num(3) + Num(4))
        self.assertEqual(reduce(Num(2)*Num(3) + Num(3) + Num(4), level=2), Num(9) + Num(4))
        self.assertEqual(reduce(Num(2)*Num(3) + Num(3) + Num(4), level=3), Num(13))
        self.assertEqual(reduce(Num(2)*Num(3) + Num(3) * Num(4)), Num(6) + Num(3)*Num(4))
        self.assertEqual(reduce(Num(2)*Num(3) + Num(3) * Num(4), level=2), Num(6) + Num(12))
        self.assertEqual(reduce(Num(2)*Num(3) + Num(3) * Num(4), level=3), Num(18))
        self.assertEqual(reduce(Num(2)*Num(3) + Num(3) * Num(4), level='max'), Num(18))

        # self.assertEqual(reduce(Div(4, 2)), Num(2))
        # self.assertEqual(reduce(Div(12, 8), Div(3, 2)))


class TestDevelope(unittest.TestCase):
    def setUp(self):
        self.one = Num(1)
        self.zero = Num(0)

    def test_develope(self):
        self.assertEqual(str(develope(self.one)), '1')
        self.assertEqual(str(develope(self.one + 2)), '1 + 2')
        self.assertEqual(str(develope(self.one * 2)), '1 * 2')
        self.assertEqual(str(develope(Num(3)*(self.zero + 1))), '0 * 3 + 1 * 3')
        self.assertEqual(str(develope((self.zero + 1)*2)), '0 * 2 + 1 * 2')
        self.assertEqual(str(develope((Num(3) - 2)*(self.zero + 1))),
                         '3 * (0 + 1) - 2 * (0 + 1)')
        self.assertEqual(str(develope((Num(3) + 4) * 2 * Num(5))), '(3 * 2 + 4 * 2) * 5')
        self.assertEqual(str(develope((Num(3) + 4) * Num(2) * Num(5), level=2)),
                         '3 * 2 * 5 + 4 * 2 * 5')
        self.assertEqual(str(develope((Num(3) - 2)*2 + Num(5)*(Num(3) - 1))),
                         '3 * 2 - 2 * 2 + 5 * (3 - 1)')
        self.assertEqual(str(develope((Num(3) - 2)*2 + Num(5)*(Num(3) - 1), level=2)),
                         '3 * 2 - 2 * 2 + 3 * 5 - 1 * 5')
        self.assertEqual(str(develope((Num(3) - 2)*2 + Num(5)*(Num(3) - 1), level=3)),
                         '3 * 2 - 2 * 2 + 3 * 5 - 1 * 5')
        # self.assertEqual(develope(Mul(2, 2) * 3), Mul(2, 2) * 3)


class TestFactorize(unittest.TestCase):
    def setUp(self):
        self.one = Num(1)
        self.zero = Num(0)

    def test_factorize(self):
        self.assertEqual(factorize(Num(2)), Num(2))
        self.assertEqual(factorize(Num(2) * Num(3)), Mul(2, 3))
        self.assertEqual(factorize(Num(4)), Mul(2, 2))
        self.assertEqual(factorize(Num(2) * Num(3) * Num(4)), Mul(2, 3) * Mul(2, 2))
        self.assertEqual(factorize(Num(2) * Num(3) * Num(4), level=0), Mul(2, 3) * Num(4))
        self.assertEqual(str(factorize(Num(2) * Num(3) * Num(4), level=4)),
                         str(Mul(2, 3) * Mul(2, 2)))
        self.assertEqual(factorize(Num(12), level=1), Num(2)*Num(6))
        print(repr(Num(2)*Num(2)*Num(3)))
        # print(repr(develope(factorize(Num(12), level=2))))
        # self.assertEqual(factorize(Num(12), level=2), Num(2)*Num(2)*Num(3))

        # self.assertEqual(str(factorize(Num(2) + Num(2))), '2*(1 + 1)')
        # self.assertEqual(str(factorize(Num(2) + Num(4))), '2*(1 + 2)')


if __name__ == '__main__':
    unittest.main()
