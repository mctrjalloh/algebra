import unittest

from context import Num, Add, reduce, develope


class TestObject(unittest.TestCase):
    def setUp(self):
        pass


class TestNum(unittest.TestCase):
    def setUp(self):
        self.n1 = Num(2)
        self.n2 = Num(3)
        self.n3 = Num(3)

    def test_str(self):
        self.assertEqual(str(self.n1), '2')

    def test_eq(self):
        self.assertTrue(self.n2 == self.n3)
        self.assertFalse(self.n1 == self.n2)

    def test_add(self):
        v1 = self.n1 + self.n2
        v2 = Add(2, 3)
        self.assertEqual(v1, v2)

    def test_sub(self):
        pass

    def test_mul(self):
        pass

    def test_truediv(self):
        pass

    def test_floordiv(self):
        pass


class TestAdd(unittest.TestCase):
    def setUp(self):
        self.add1 = Add(2, 3)
        self.add2 = Add(2, 3)
        self.add3 = Add(3, 4)

    def test_str(self):
        self.assertEqual(str(self.add1), '2 + 3')

    def test_eq(self):
        self.assertEqual(self.add1, self.add2)

    def test_add(self):
        add1 = self.add1 + self.add3
        add2 = self.add1 + Num(6)
        self.assertEqual(add1, Add(5, 7))
        self.assertEqual(add2, Add(5, 6))

    def test_sub(self):
        pass


class TestReduce(unittest.TestCase):
    def setUp(self):
        self.one = Num(1)
        self.zero = Num(0)

    def test_(self):
        self.assertEqual(str(reduce(Num(4))), '4')
        self.assertEqual(str(reduce(Num(2) + Num(3))), '5')
        self.assertEqual(str(reduce(Num(2) * Num(3))), '6')
        self.assertEqual(str(reduce(Num(2) * Num(3) + Num(4), level=4)), '10')
        self.assertEqual(str(reduce(self.one * 2 + 3)), '2 + 3')
        self.assertEqual(str(reduce(self.one * 2 * -1, level=2)), '-2')
        self.assertEqual(str(reduce(Num(2)*Num(3) + Num(3) + Num(4))), '6 + 3 + 4')
        self.assertEqual(str(reduce(Num(2)*Num(3) + Num(3) + Num(4), level=2)), '9 + 4')
        self.assertEqual(str(reduce(Num(2)*Num(3) + Num(3) + Num(4), level=3)), '13')
        self.assertEqual(str(reduce(Num(2)*Num(3) + Num(3) * Num(4))), '6 + 3 * 4')
        self.assertEqual(str(reduce(Num(2)*Num(3) + Num(3) * Num(4), level=2)), '6 + 12')
        self.assertEqual(str(reduce(Num(2)*Num(3) + Num(3) * Num(4), level=3)), '18')


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


class TestFactorize(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
