from abc import *


class Input:
    def __init__(self, owner):
        super().__init__()
        self._value = None
        if owner is LogicGate:
            self._owner = owner
        else:
            raise Exception("Invalid type")

    def __str__(self):
        return str(self._value)

    @property
    def get_owner(self):
        return self._owner

    @property
    def in_value(self):
        return self._value

    @in_value.setter
    def in_value(self, value):
        self._value = bool(value)


class Output:
    def __init__(self):
        self._connections = []
        self._value = None

    def __str__(self):
        return str(self._value)

    @property
    def get_connections(self):
        return self._connections

    @property
    def out_value(self):
        return self._value

    @out_value.setter
    def out_value(self, value):
        self._value = bool(value)

    def connect(self, inp):
        if isinstance(inp, Input):
            if inp not in self._connections:
                inp._value = self._value
                self.get_connections.append(input)
        else:
            raise Exception("Invalid type")


class CostMixin:
    COST_MULTIPLIER = 10

    def __init__(self, number_of_components):
        self._number_of_components = number_of_components
        self._cost = self.COST_MULTIPLIER * (number_of_components ** 2)

    @property
    def num_components(self):
        return self._number_of_components

    @property
    def get_cost(self):
        return self._cost


class NodeMixin(CostMixin):
    def __init__(self, number_of_components):
        super().__init__(number_of_components)
        self._next = None

    @property
    def node_next(self):
        return self._next

    @node_next.setter
    def node_next(self, n):
        if isinstance(n, NodeMixin):
            self._next = n
        else:
            raise Exception("invalid type")


class Circuit:
    def __init__(self):
        self._cost = 0
        self._top_of_list = NodeMixin(0)

    def add(self, gate):
        if isinstance(gate, LogicGate):
            gate.node_next = self._top_of_list
            self._top_of_list = gate
        else:
            raise Exception("invalid gate")

    def evaluate_cost(self):
        while self._top_of_list is not None:
            self._cost += self._top_of_list.get_cost
            self._top_of_list = self._top_of_list.node_next

    @property
    def get_cost(self):
        return self._cost


class LogicGate(ABC, NodeMixin):
    def __init__(self, name, num):
        NodeMixin.__init__(self, num)
        self.node_next = NodeMixin(num)
        self._name = name
        self._output = Output()
        self._input = Input(LogicGate)
        self._input0 = Input(LogicGate)
        self._input1 = Input(LogicGate)

    @abstractmethod
    def __str__(self):
        return "Gate {}:".format(self.get_name)

    @property
    def get_name(self):
        return self._name

    @property
    def get_input(self):
        return self._input

    @property
    def get_input0(self):
        return self._input0

    @property
    def get_input1(self):
        return self._input1

    @property
    def get_output(self):
        return self._output

    @abstractmethod
    def evaluate(self):
        if self.get_input.in_value is not None:
            self.get_input.in_value = self.get_input.in_value
        elif self.get_input0.in_value is not None and self.get_input1.in_value is not None:
            self.get_input0.in_value = self.get_input0.in_value
            self.get_input1.in_value = self.get_input1.in_value


class NotGate(LogicGate, NodeMixin):
    NOT_GATE_COMPONENTS = 2

    def __init__(self, name, circuit=None):
        LogicGate.__init__(self, name, self.NOT_GATE_COMPONENTS)
        if isinstance(circuit, Circuit):
            self.circuit = circuit
        self.evaluate()

    def __str__(self):
        return super().__str__() + " input={0}, output={1}" \
            .format(self.get_input.in_value, self.get_output.out_value)

    def evaluate(self):
        super().evaluate()
        if self.get_input.in_value:
            self.get_output.out_value = False
        elif self.get_input.in_value is False:
            self.get_output.out_value = True


class AndGate(LogicGate, NodeMixin):
    AND_GATE_COMPONENTS = 8

    def __init__(self, name, circuit=None):
        LogicGate.__init__(self, name, self.AND_GATE_COMPONENTS)
        if isinstance(circuit, Circuit):
            self._circuit = circuit

    def __str__(self):
        return super().__str__() + " input0={0}, input1={1}, output={2}" \
            .format(self.get_input0.in_value, self.get_input1.in_value, self.get_output.out_value)

    def evaluate(self):
        super().evaluate()
        if self.get_input0.in_value and self.get_input1.in_value:
            self.get_output.out_value = True
        elif self.get_input0.in_value is False or self.get_input1.in_value is False:
            self.get_output.out_value = False


class OrGate(AndGate):
    def __init__(self, name, circuit=None):
        LogicGate.__init__(self, name, self.AND_GATE_COMPONENTS)
        if isinstance(circuit, Circuit):
            self._circuit = circuit

    def evaluate(self):
        if self.get_input0.in_value or self.get_input1.in_value:
            self.get_output.out_value = True
        else:
            self.get_output.out_value = False


class XorGate(AndGate):
    def __init__(self, name, circuit=None):
        LogicGate.__init__(self, name, self.AND_GATE_COMPONENTS)
        if isinstance(circuit, Circuit):
            self._circuit = circuit

    def evaluate(self):
        if (self.get_input0.in_value and self.get_input1.in_value) \
                or (self.get_input0.in_value is False and self.get_input1.in_value is False):
            self.get_output.out_value = False
        else:
            self.get_output.out_value = True


def full_adder(a, b, ci):
    circuit = Circuit()
    xor_gate1 = XorGate("xor1", circuit)
    xor_gate2 = XorGate("xor2", circuit)
    and_gate1 = AndGate("and1", circuit)
    and_gate2 = AndGate("and2", circuit)
    or_gate = OrGate("or", circuit)

    circuit.add(xor_gate1)
    circuit.add(xor_gate2)
    circuit.add(and_gate1)
    circuit.add(and_gate2)
    circuit.add(or_gate)
    circuit.evaluate_cost()

    # a xor b
    xor_gate1.get_input0.in_value = a
    xor_gate1.get_input1.in_value = b
    xor_gate1.evaluate()

    # (a xor b) xor ci
    xor_gate1.get_output.connect(xor_gate2.get_input0)
    xor_gate2.get_input1.in_value = ci
    xor_gate2.evaluate()

    # sum result
    x = xor_gate2.get_output.out_value

    # (a xor b) and ci
    xor_gate1.get_output.connect(and_gate1.get_input0)
    and_gate1.get_input1.in_value = ci
    and_gate1.evaluate()

    # a and b
    and_gate2.get_input0.in_value = a
    and_gate2.get_input1.in_value = b
    and_gate2.evaluate()

    # ((a￿ xor ￿b)￿ and ￿ci)￿ or (a￿ and b)
    and_gate1.get_output.connect(or_gate.get_input0)
    and_gate2.get_output.connect(or_gate.get_input1)
    or_gate.evaluate()

    # co result
    y = or_gate.get_output.out_value

    # circuit cost
    z = circuit.get_cost
    return str(x), str(y), str(z)
