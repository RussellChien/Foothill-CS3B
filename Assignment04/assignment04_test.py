import unittest
from assignment04 import *


class LogicGatesTest(unittest.TestCase):
    def test_not_gate(self):
        not_gate = NotGate("not")
        expected = str(not_gate)
        self.assertEqual(expected, "Gate not: input=None, output=None")
        not_gate.get_input.in_value = True
        not_gate.evaluate()
        self.assertEqual(str(not_gate), "Gate not: input=True, output=False")
        not_gate.get_input.in_value = False
        not_gate.evaluate()
        self.assertEqual(str(not_gate), "Gate not: input=False, output=True")

    def test_and_gate(self):
        and_gate = AndGate("and")
        self.assertEqual(str(and_gate), "Gate and: input0=None, input1=None, output=None")
        and_gate.get_input0.in_value = False
        and_gate.get_input1.in_value = False
        and_gate.evaluate()
        self.assertEqual(str(and_gate), "Gate and: input0=False, input1=False, output=False")
        and_gate.get_input0.in_value = True
        and_gate.evaluate()
        self.assertEqual(str(and_gate), "Gate and: input0=True, input1=False, output=False")
        and_gate.get_input1.in_value = True
        and_gate.evaluate()
        self.assertEqual(str(and_gate), "Gate and: input0=True, input1=True, output=True")

    def test_or_gate(self):
        or_gate = OrGate("or")
        self.assertEqual(str(or_gate), "Gate or: input0=None, input1=None, output=None")
        or_gate.get_input0.in_value = False
        or_gate.get_input1.in_value = False
        or_gate.evaluate()
        self.assertEqual(str(or_gate), "Gate or: input0=False, input1=False, output=False")
        or_gate.get_input0.in_value = True
        or_gate.evaluate()
        self.assertEqual(str(or_gate), "Gate or: input0=True, input1=False, output=True")
        or_gate.get_input1.in_value = True
        or_gate.evaluate()
        self.assertEqual(str(or_gate), "Gate or: input0=True, input1=True, output=True")

    def test_xor_gate(self):
        xor_gate = XorGate("xor")
        actual = "Gate xor: input0=None, input1=None, output=None"
        self.assertEqual(str(xor_gate), actual)
        xor_gate.get_input0.in_value = False
        xor_gate.get_input1.in_value = False
        xor_gate.evaluate()
        self.assertEqual(str(xor_gate), "Gate xor: input0=False, input1=False, output=False")
        xor_gate.get_input0.in_value = True
        xor_gate.evaluate()
        self.assertEqual(str(xor_gate), "Gate xor: input0=True, input1=False, output=True")
        xor_gate.get_input1.in_value = True
        xor_gate.evaluate()
        self.assertEqual(str(xor_gate), "Gate xor: input0=True, input1=True, output=False")

    def test_connect(self):
        not_gate1 = NotGate("not1")
        not_gate2 = NotGate("not2")
        not_gate1.get_input.in_value = False
        not_gate1.evaluate()
        self.assertEqual(str(not_gate1), "Gate not1: input=False, output=True")
        not_gate1.get_output.connect(not_gate2.get_input)
        not_gate2.evaluate()
        self.assertEqual(str(not_gate2), "Gate not2: input=True, output=False")
        not_gate1.get_input.in_value = True
        not_gate1.evaluate()
        not_gate1.get_output.connect(not_gate2.get_input)
        not_gate2.evaluate()
        self.assertEqual(str(not_gate2), "Gate not2: input=False, output=True")

    def test_connect1(self):
        not_gate = NotGate("not")
        and_gate = AndGate("and")
        not_gate.get_input.in_value = False
        not_gate.evaluate()
        self.assertEqual(str(not_gate), "Gate not: input=False, output=True")
        not_gate.get_output.connect(and_gate.get_input0)
        and_gate.evaluate()
        self.assertEqual(str(and_gate), "Gate and: input0=True, input1=None, output=None")
        not_gate.get_output.connect(and_gate.get_input1)
        and_gate.evaluate()
        self.assertEqual(str(and_gate), "Gate and: input0=True, input1=True, output=True")
        not_gate.get_input.in_value = True
        not_gate.evaluate()
        self.assertEqual(str(not_gate), "Gate not: input=True, output=False")
        not_gate.get_output.connect(and_gate.get_input0)
        and_gate.evaluate()
        self.assertEqual(str(and_gate), "Gate and: input0=False, input1=True, output=False")

    def test_connect2(self):
        not_gate = NotGate("not")
        or_gate = OrGate("or")
        not_gate.get_input.in_value = False
        not_gate.evaluate()
        self.assertEqual(str(not_gate), "Gate not: input=False, output=True")
        not_gate.get_output.connect(or_gate.get_input0)
        or_gate.evaluate()
        self.assertEqual(str(or_gate), "Gate or: input0=True, input1=None, output=True")
        not_gate.get_output.connect(or_gate.get_input1)
        or_gate.evaluate()
        self.assertEqual(str(or_gate), "Gate or: input0=True, input1=True, output=True")
        not_gate.get_input.in_value = True
        not_gate.evaluate()
        self.assertEqual(str(not_gate), "Gate not: input=True, output=False")
        not_gate.get_output.connect(or_gate.get_input0)
        or_gate.evaluate()
        self.assertEqual(str(or_gate), "Gate or: input0=False, input1=True, output=True")

    def test_connect2(self):
        not_gate = NotGate("not")
        xor_gate = XorGate("xor")
        not_gate.get_input.in_value = False
        not_gate.evaluate()
        self.assertEqual(str(not_gate), "Gate not: input=False, output=True")
        not_gate.get_output.connect(xor_gate.get_input0)
        xor_gate.evaluate()
        self.assertEqual(str(xor_gate), "Gate xor: input0=True, input1=None, output=True")
        not_gate.get_output.connect(xor_gate.get_input1)
        xor_gate.evaluate()
        self.assertEqual(str(xor_gate), "Gate xor: input0=True, input1=True, output=False")
        not_gate.get_input.in_value = True
        not_gate.evaluate()
        self.assertEqual(str(not_gate), "Gate not: input=True, output=False")
        not_gate.get_output.connect(xor_gate.get_input0)
        xor_gate.evaluate()
        self.assertEqual(str(xor_gate), "Gate xor: input0=False, input1=True, output=True")


