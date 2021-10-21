import math
import numpy as np


def main():
    valid_rule_given = False
    while not valid_rule_given:
        try:
            rule = int(input("Enter Rule ({} - {}): ".format(Automaton.MIN_RULE, Automaton.MAX_RULE)))
            if not (Automaton.MIN_RULE <= rule <= Automaton.MAX_RULE):
                print("** please enter an integer in the specified range **")
            else:
                valid_rule_given = True
        except (TypeError, ValueError) as err:
            print("** {} \n   please enter an integer in the specified range.\n".format(err))
    aut = Automaton(rule)
    for k in range(50):
        print(aut.to_string_current_gen())
        aut.propagate_new_generation()


class Automaton:
    RULES_SIZE = 8
    BITS_IN_RULE_SIZE = int(math.log(RULES_SIZE, 2))  # 3
    MIN_DISPLAY_WIDTH = 20
    MAX_DISPLAY_WIDTH = 121
    DFLT_DISPLAY_WIDTH = 79
    MIN_RULE = 0
    MAX_RULE = 2 ** RULES_SIZE - 1  # 255
    DFLT_RULE = 126
    ON_STR = "*"
    OFF_STR = " "

    def __init__(self, rule=DFLT_RULE):
        self.extreme_bit = self.OFF_STR
        self.this_gen = self.ON_STR
        self.display_width = self.set_display_width()
        self.rule = np.empty(8, dtype=bool)
        self.set_rule(rule)
        self.reset_first_gen()

    def set_rule(self, rule):
        binary_str = "{:08b}".format(rule)
        self.rule = np.array([int(i) == 1 for i in binary_str[::-1]])

    def reset_first_gen(self):
        self.extreme_bit = self.OFF_STR
        self.this_gen = self.ON_STR

    def propagate_new_generation(self):
        temp = self.extreme_bit + self.extreme_bit + self.this_gen + self.extreme_bit + self.extreme_bit
        next_gen = ""
        for i in range(1, len(temp) - 1):
            triplet = temp[i - 1:i + 2]
            bin_num = ""
            for j in triplet:
                if j == self.OFF_STR:
                    bin_num += "0"
                else:
                    bin_num += "1"
            int_bin_num = int(bin_num, 2)
            if self.rule[int_bin_num]:
                next_gen += self.ON_STR
            else:
                next_gen += self.OFF_STR
            self.this_gen = next_gen
            if self.extreme_bit == self.OFF_STR:
                if self.rule[0]:
                    self.extreme_bit = self.ON_STR
            else:  # if self.extreme_bit == self.ON_STR
                if not self.rule[7]:
                    self.extreme_bit = self.OFF_STR

    def to_string_current_gen(self):
        diff = self.display_width - len(self.this_gen)
        if diff < 0:
            extra_space = -(diff // 2)
            return self.this_gen[extra_space:len(self.this_gen) - extra_space]
        elif diff > 0:
            padding = diff // 2
            pad = ""
            for i in range(padding):
                pad += self.extreme_bit
            return pad + self.this_gen + pad
        else:
            return self.this_gen

    def set_display_width(self, width=DFLT_DISPLAY_WIDTH):
        if width % 2 == 1 and self.MIN_DISPLAY_WIDTH <= width <= self.MAX_DISPLAY_WIDTH:
            return width


if __name__ == "__main__":
    main()
