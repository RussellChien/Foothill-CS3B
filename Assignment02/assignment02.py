import copy
import numpy


def main():
    test()


class MyStack:
    MAX_SIZE = 100000
    DEFAULT_SIZE = 10
    EMPTY_STACK_RETURN_ALERT = "Failed. Attempt to pop from empty stack"
    ORIG_DEFAULT_ITEM = 0
    default_item = ORIG_DEFAULT_ITEM

    def __init__(self, capacity=DEFAULT_SIZE, default_item=None):

        self.tos = 0  # Top of stack
        self.stack = []  # Empty stack
        if not self.set_capacity(capacity):
            self.capacity = MyStack.DEFAULT_SIZE

        if default_item is not None:
            self.default_item = default_item
        self.clear()

    def set_capacity(self, capacity):
        if not MyStack.valid_capacity(capacity):
            return False
        self.capacity = capacity
        self.clear()
        return True

    def push(self, item_to_push):
        if self.tos == self.capacity:
            return False
        self.stack[self.tos] = item_to_push
        self.tos += 1
        return True

    def pop(self):
        if self.tos == 0:
            return self.EMPTY_STACK_RETURN_ALERT
        self.tos -= 1
        return self.stack[self.tos]

    def clear(self):
        self.stack = numpy.array([copy.deepcopy(self.default_item)
                                  for k in range(self.capacity)])
        self.tos = 0

    def get_capacity(self):
        return self.capacity

    @classmethod
    def valid_capacity(cls, test_capacity):
        if not (0 <= test_capacity <= cls.MAX_SIZE):
            return False
        else:
            return True

    @classmethod
    def set_default_item(cls, new_default):
        cls.default_item = new_default


class Rpncalculator:
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "//"
    OPS = [ADDITION, SUBTRACTION, MULTIPLICATION, DIVISION]

    @staticmethod
    def eval(rpn_expression):
        expression = Rpncalculator.parse(rpn_expression)
        return Rpncalculator.eval_tokens(expression)

    @staticmethod
    def parse(rpn_expression):
        return rpn_expression.split()

    @staticmethod
    def eval_tokens(tokens):
        stack = MyStack(10)
        calculated = False
        for i in tokens:
            try:
                stack.push(int(i))
            except ValueError:
                if i not in Rpncalculator.OPS:
                    raise Exception("Invalid operator.")
                elif stack.tos == 0 and i in Rpncalculator.OPS:
                    raise Exception("This is postfix notation; numbers go before operator.")
                elif stack.tos < 2:
                    raise Exception("Insufficient numbers in expression.")
                else:
                    num1 = stack.pop()
                    num2 = stack.pop()
                    calculated = True
                    if i == Rpncalculator.ADDITION:
                        stack.push(num1 + num2)
                    elif i == Rpncalculator.SUBTRACTION:
                        stack.push(num1 - num2)
                    elif i == Rpncalculator.MULTIPLICATION:
                        stack.push(Rpncalculator.multiply(num1, num2))
                    elif i == Rpncalculator.DIVISION:
                        stack.push(num1 // num2)
        if stack.tos == 1 and calculated:
            return stack.pop()
        else:
            raise Exception("Insufficient operators in expression.")

    @staticmethod
    def multiply(a, b):
        if b == 0:
            return 0
        elif b < 0:
            return -a + Rpncalculator.multiply(a, b + 1)
        elif b > 0:
            return a + Rpncalculator.multiply(a, b - 1)


def test():
    test_list = ["3", "2 3 +", "2 3 -", "2 3 *", "2 3 //",
                 "2 3 4 + *", "2 3 4 + -", "2 3 4 + +",
                 " ", "1 +", "1 1", "1 1 fly", "2 -4 2 * //",
                 "-1 2 7 -10 * + -", "5 -6 8 2 3 * // - +",
                 "+ - *", "test", "+ 1 2", ]

    for i in test_list:
        try:
            print(i, "=", Rpncalculator.eval(i))
        except Exception as e:
            print(i, "Failed. {}".format(e))


if __name__ == '__main__':
    main()
