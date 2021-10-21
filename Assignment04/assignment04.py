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

    def connect(self, input):
        if isinstance(input, Input):
            if input not in self._connections:
                input._value = self._value
        else:
            raise Exception("Invalid type")


class LogicGate:
    def __init__(self, name):
        self._name = name
        self._output = Output()
        self._input = Input(LogicGate)
        self._input0 = Input(LogicGate)
        self._input1 = Input(LogicGate)

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

    def evaluate(self):
        if self.get_input.in_value is not None:
            self.get_input.in_value = self.get_input.in_value
        elif self.get_input0.in_value is not None and self.get_input1.in_value is not None:
            self.get_input0.in_value = self.get_input0.in_value
            self.get_input1.in_value = self.get_input1.in_value


class NotGate(LogicGate):
    def __init__(self, name):
        super().__init__(name)
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


class AndGate(LogicGate):
    def __init__(self, name):
        super().__init__(name)

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
    def __init__(self, name):
        super().__init__(name)

    def evaluate(self):
        if self.get_input0.in_value or self.get_input1.in_value:
            self.get_output.out_value = True
        else:
            self.get_output.out_value = False


class XorGate(AndGate):
    def __init__(self, name):
        super().__init__(name)

    def evaluate(self):
        if (self.get_input0.in_value and self.get_input1.in_value) \
                or (self.get_input0.in_value is False and self.get_input1.in_value is False):
            self.get_output.out_value = False
        else:
            self.get_output.out_value = True
