from assignment07 import *


def test0():
    bf_a = BooleanFunc()
    bf_b = BooleanFunc(13)
    bf_c = BooleanFunc(100, eval_return_if_error=True)
    bf_d = BooleanFunc(21, defining_list=21 * [3.1])
    bf_e = BooleanFunc(2, eval_return_if_error=True, defining_list=[False, True])

    print("{}\n{}\n{}\n{}\n{}".format(bf_a, bf_b, bf_c, bf_d, bf_e))

    bf_and = BooleanFunc(defining_list=[0, 0, 0, 1])
    print("the AND gate using ints:\n", bf_and, "\n")

    bf_and = BooleanFunc(defining_list=[False, False, False, True])
    print("the AND gate using bools:\n", bf_and, "\n")

    try:
        bf_bad = BooleanFunc(21, defining_list=1.11)
    except Exception as err:
        print(type(err), ":", err, "\n")

    try:
        bf_bad = BooleanFunc(21, defining_list=[False, True])
    except Exception as err:
        print(type(err), ":", err, "\n")

    try:
        bf_bad = BooleanFunc(6, defining_list="hi mom")
        print(bf_bad)
    except Exception as err:
        print(type(err), ":", err, "\n")


# Act 1 test
def test1():
    bf_and = BooleanFunc(defining_list=[False, False, False, True])
    even_func_w_errs_true = [0, "bad", 2, 4, 6, 8, 10, 12, 3.14, 14]
    greater_9_func_true = [10, 11, 12, 13, 14, 15]
    greater_3_func_false = [0, 1, 2, 3]

    bf_a = BooleanFunc(10)
    bf_b = BooleanFunc(16)
    bf_c = BooleanFunc(16)

    print("--- Testing constructors and mutators of AND, even, >9 and >3 ---")
    bf_a.set_truth_table_using(True, even_func_w_errs_true)
    bf_b.set_truth_table_using(True, greater_9_func_true)
    bf_c.set_truth_table_using(False, greater_3_func_false)

    for func in [bf_and, bf_a, bf_b, bf_c]:
        print(func)

    print("--- Testing intputs that cover the allowable and illegal values for AND ---")
    for input_x in range(10):
        print(bf_and.eval(input_x))
        print("AND({}) = {}".format(input_x, bf_and.get_state()))


# Act 2 test
def test2():
    my_12_seg = MultiSegmentLogic(12)

    print("As constructed -------------------")
    print(my_12_seg)

    try:
        my_12_seg.eval(1)
    except AttributeError as err:
        print("\nExpected ... " + str(err) + "\n")

    for k in range(12):
        my_12_seg.set_segment(k, BooleanFunc(
            defining_list=[True, False, True, False]))

    print(my_12_seg)

    print("Evaluating my_12_seg at 2 (which should be True) -----------")
    my_12_seg.eval(2)
    print(my_12_seg.get_val_of_seg(2))
    print()
    print("segs 3, 5 and, illegal, 29:   ",
          str(my_12_seg.get_val_of_seg(3)),
          str(my_12_seg.get_val_of_seg(5)),
          str(my_12_seg.get_val_of_seg(29))
          )


# Act 3 test
def test3():
    my_7_seg = SevenSegmentLogic()

    print("As constructed -------------------")
    print(my_7_seg)

    try:
        my_7_seg.set_num_segs(8)  # should "throw"
    except ValueError as err:
        print("\nExpected ... " + str(err) + "\n")

    try:
        my_7_seg.eval(1)
    except AttributeError as err:
        print("\nNot Expected... " + str(err) + "\n")

    for input_x in range(16):
        my_7_seg.eval(input_x)
        print("\n| ", end='')
        for k in range(7):
            print(str(my_7_seg.get_val_of_seg(k)) + " | ", end='')
        print()


if __name__ == '__main__':
    test0()
    test1()
    test2()
    test3()
