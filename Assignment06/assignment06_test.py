import unittest
import copy
from CS3B.assignment06 import Complex


class ComplexTest(unittest.TestCase):
    def test_negative(self):
        complex1 = Complex(45, 5)
        result1 = -complex1
        actual1 = "(-45, -5)"
        self.assertEqual(str(result1), actual1)

    def test_addition(self):
        complex1 = Complex(1, 2)
        complex2 = Complex(3, 4)
        result1 = complex1 + complex2
        actual1 = "(4, 6)"
        self.assertEqual(str(result1), actual1)
        result2 = complex1 + 2
        actual2 = "(3, 2)"
        self.assertEqual(str(result2), actual2)
        result3 = 6 + complex2
        actual3 = "(9, 4)"
        self.assertEqual(str(result3), actual3)
        result4 = 2 + 3
        actual4 = "5"
        self.assertEqual(str(result4), actual4)

    def test_subtraction(self):
        complex1 = Complex(1, 2)
        complex2 = Complex(3, 4)
        result1 = complex1 - complex2
        actual1 = "(-2, -2)"
        self.assertEqual(str(result1), actual1)
        result2 = 3 - 4
        actual2 = '-1'
        self.assertEqual(str(result2), actual2)

    def test_multiplication(self):
        complex1 = Complex(3, 4)
        complex2 = Complex(7, 2)
        result1 = complex1 * complex2
        actual1 = "(13, 34)"
        self.assertEqual(str(result1), actual1)
        result2 = complex2 * 3
        actual2 = "(21, 6)"
        self.assertEqual(str(result2), actual2)
        result3 = 3 * complex2
        actual3 = "(21, 6)"
        self.assertEqual(str(result3), actual3)

    def test_division(self):
        complex1 = Complex(4, 6)
        complex2 = Complex(1, 3)
        result1 = complex1 / complex2
        actual1_real = -0.613940613515
        actual1_imag = -0.78935221737
        self.assertAlmostEqual(result1.real, actual1_real)
        self.assertAlmostEqual(result1.imag, actual1_imag)
        result2 = complex2 / 3
        actual2_real = 0.31622776602
        actual2_imag = -0.9486832980
        self.assertAlmostEqual(result2.real, actual2_real)
        self.assertAlmostEqual(result2.imag, actual2_imag)

    def test_equal(self):
        complex1 = Complex(7, 7)
        complex2 = Complex(7, 7)
        result1 = complex1 == complex2
        actual1 = True
        self.assertEqual(result1, actual1)
        complex3 = Complex(3, 0)
        result2 = complex3 == 3
        actual2 = True
        self.assertEqual(result2, actual2)

    def test_less_than(self):
        complex1 = Complex(1, 2)
        complex2 = Complex(3, 4)
        result1 = complex1 < complex2
        actual1 = True
        self.assertEqual(result1, actual1)
        result2 = complex1 < 9
        actual2 = True
        self.assertEqual(result2, actual2)

    def test_shallow_copy(self):
        complex_list = [Complex(k, k) for k in range(0, 10)]
        shallow_list = copy.copy(complex_list)
        for i in range(0, 10):
            self.assertEqual(id(complex_list[i]), id(shallow_list[i]))
        self.assertNotEqual(id(complex_list), id(shallow_list))
        deep_list = copy.deepcopy(complex_list)
        for i in range(0, 10):
            self.assertNotEqual(id(complex_list[i]), id(deep_list[i]))
        self.assertNotEqual(id(complex_list), id(deep_list))
