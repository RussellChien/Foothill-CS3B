import math


class Complex:
    def __init__(self, real=0, imag=0):
        self._real = real
        self._imag = imag

    def __str__(self):
        return "({0}, {1})".format(self.real, self.imag)

    @property
    def reciprocal(self):
        try:
            return Complex(self.real / math.sqrt(self.real ** 2 + self.imag ** 2),
                           -self.imag / math.sqrt(self.real ** 2 + self.imag ** 2))
        except ZeroDivisionError as e:
            return e

    @property
    def real(self):
        return self._real

    @real.setter
    def real(self, real_num):
        try:
            self.real = real_num
        except TypeError as e:
            raise e

    @property
    def imag(self):
        return self._imag

    @imag.setter
    def imag(self, imag_num):
        try:
            self.imag = imag_num
        except TypeError as e:
            raise e

    @property
    def modulus(self):
        return math.sqrt(self.real ** 2 + self.imag ** 2)

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        return Complex(self.real * other.real - self.imag * other.imag,
                       self.real * other.imag + other.real * self.imag)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self.__mul__(other).reciprocal

    def __rtruediv__(self, other):
        return self / other

    def __neg__(self):
        return Complex(-self.real, -self.imag)

    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    def __lt__(self, other):
        return self.modulus < Complex(other.real, other.imag).modulus
