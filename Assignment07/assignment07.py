import numpy as np
import copy


class BooleanFunc:
    MAX_TABLE_SIZE = 65536
    MIN_TABLE_SIZE = 2
    DEFAULT_TABLE_SIZE = 4
    DEFAULT_FUNC = DEFAULT_TABLE_SIZE * [False]

    def __init__(self, table_size=None, defining_list=None, eval_return_if_error=False):
        if not table_size and not defining_list:
            # passed neither list nor size
            table_size = self.DEFAULT_TABLE_SIZE
            defining_list = self.DEFAULT_FUNC
        elif table_size and not defining_list:
            # passed size but no list
            self.valid_table_size(table_size)  # raises, no return
            defining_list = table_size * [False]
        elif not table_size:
            # passed list but no size
            self.valid_defining_list(defining_list)  # raises, no return
            table_size = len(defining_list)
        else:
            # passed both list and size
            self.valid_defining_list(defining_list)
            if len(defining_list) != table_size:
                raise ValueError("Table size does not match list length in constructor.")

        # sanitize bools (e.g. (1.32, "hi", -99)->True,
        # (0.0, "", 0)->False)
        eval_return_if_error = bool(eval_return_if_error)
        defining_list = [bool(item) for item in defining_list]

        self.eval_return_if_error = eval_return_if_error
        self.state = eval_return_if_error
        self.table_size = table_size
        self.truth_table = np.array(defining_list, dtype=bool)

    def __str__(self):
        ret_str = "truth_table: " + str(self.truth_table) \
                  + "\nsize = " + str(self.table_size) \
                  + "\nerror return = " + str(self.eval_return_if_error) \
                  + "\ncurrent state = " + str(self.state) + "\n"
        return ret_str

    def eval(self, input):
        if input <= self.truth_table.size - 1 and type(input) == int:
            self.state = self.truth_table[input]
        else:
            self.state = self.eval_return_if_error
        return self.state

    def get_state(self):
        return self.state

    @property
    def get_eval_return_if_error(self):
        return self.eval_return_if_error

    @classmethod
    def valid_table_size(cls, size):
        if not isinstance(size, int):
            raise TypeError("Table size must be an int.")
        if not (cls.MIN_TABLE_SIZE <= size <= cls.MAX_TABLE_SIZE):
            raise ValueError("Bad table size passed to constructor (legal range: {}-{}).".
                             format(cls.MIN_TABLE_SIZE, cls.MAX_TABLE_SIZE))

    @classmethod
    def valid_defining_list(cls, the_list):
        if not isinstance(the_list, list):
            raise ValueError("Bad type in constructor. defining_list must be type list.")
        if not (cls.MIN_TABLE_SIZE <= len(the_list) <= cls.MAX_TABLE_SIZE):
            raise ValueError("Bad list passed to constructor (its length is outside legal range: {}-{}).".
                             format(cls.MIN_TABLE_SIZE, cls.MAX_TABLE_SIZE))

    def set_truth_table_using(self, rarer_value, rarer_val_lst):
        if type(rarer_value) is bool and len(rarer_val_lst) <= self.truth_table.size:
            for i in range(self.truth_table.size):
                if i not in rarer_val_lst:
                    self.truth_table[i] = not rarer_value
                else:
                    self.truth_table[i] = rarer_value
            return True
        else:
            return False


class MultiSegmentLogic:
    MAX_SEGS = 1000  # inclusive
    MIN_SEGS = 1  # inclusive
    DEFAULT_SEGS = 7

    def __init__(self, num_segs=DEFAULT_SEGS):
        self.num_segs = num_segs
        self.set_num_segs(num_segs)

    def __str__(self):
        ret_str = []
        for seg in self.segs:
            if seg is not None:
                ret_str.append("truth_table: " + str(seg.truth_table) +
                               "\nsize = " + str(seg.table_size)
                               + "\nerror return = " + str(seg.get_eval_return_if_error)
                               + "\ncurrent state = " + str(seg.state) + "\n")
        return str(ret_str)

    def set_num_segs(self, num_segs):
        if self.MIN_SEGS <= num_segs <= self.MAX_SEGS:
            self.segs = np.array([None for i in range(num_segs)])

    def set_segment(self, seg_num, func_for_this_seg):
        if isinstance(func_for_this_seg, BooleanFunc) and isinstance(seg_num, int) \
                and 0 <= seg_num <= self.num_segs - 1:
            self.segs[seg_num] = copy.deepcopy(func_for_this_seg)
            return True
        else:
            return False

    def eval(self, input):
        for seg in self.segs:
            i = 1
            if seg is None:
                raise AttributeError('Segment at index {} is not set'.format(i))
            i += 1
            seg.eval(input)

    def get_val_of_seg(self, seg_num):
        if self.MIN_SEGS <= seg_num <= self.num_segs - 1 and isinstance(seg_num, int):
            return self.segs[seg_num].state
        else:
            return False


class SevenSegmentLogic(MultiSegmentLogic):
    def __init__(self):
        super().__init__(7)

    def set_num_segs(self, num_segs):
        if num_segs == 7:
            super().set_num_segs(num_segs)
            self.initialize_array()
        else:
            raise ValueError("Number of segments not equal to 7")

    def get_val_of_seg(self, k):
        if 0 <= self.num_segs <= 7:
            return self.segs[k].state
        else:
            return False

    def initialize_array(self):
        exception_list = [[1, 4, 11, 13], [5, 6, 11, 12, 14, 15], [2, 12, 14, 15], [1, 4, 7, 9, 10, 15],
                          [1, 3, 4, 5, 7, 9], [1, 2, 3, 7, 13], [0, 1, 7, 12]]
        for i in range(0, 7):
            bf_for_seg = BooleanFunc(16)
            bf_for_seg.set_truth_table_using(False, exception_list[i])
            self.set_segment(i, bf_for_seg)
