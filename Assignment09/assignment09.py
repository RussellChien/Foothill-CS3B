import string
from tree import *


class FhTreeNode:
    def __init__(self, sib=None, first_child=None, prev=None, root=None, label=None):
        self.sib = sib
        self.first_child = first_child
        self.prev = prev
        self.my_root = root

        self.label = label

    def __str__(self):
        return f"Node (label={self.label}, id={id(self):#x})"


class FhTree:
    def __init__(self):
        self.clear()
        self.m_root = None
        self.m_size = 0

    def clear(self):
        self.m_root = None
        self.m_size = 0

    def valid_node(self, node):
        if not isinstance(node, FhTreeNode):
            return TypeError("node should be FhTreeNode")

    def valid_node_in_tree(self, node):
        self.valid_node(node)

        if self.m_root is not node.my_root:
            return ValueError("node is not in the same tree")

    def set_root(self, root):
        self.valid_node(root)

        self.m_root = root
        self.m_size = 1
        root.my_root = root

    def add_node(self, parent, child):
        self.valid_node_in_tree(parent)
        self.valid_node(child)

        child.sib = parent.first_child
        child.first_child = None
        child.prev = parent
        child.my_root = self.m_root

        parent.first_child = child
        if child.sib:
            child.sib.prev = child

        self.m_size += 1

    BLANK = "  "

    def __str__(self):
        return f"--- beginning of tree, size={self.size()} ---\n" + \
               self.str_recurse(self.m_root, 0) + \
               "--- end of tree ---"

    def str_recurse(self, node, depth):
        if not node:
            return ""

        ret_str = self.BLANK * depth + str(node) + "\n"

        ret_str += self.str_recurse(node.first_child, depth + 1)
        ret_str += self.str_recurse(node.sib, depth)

        return ret_str

    def remove_node(self, node):
        self.remove_node_recurse(node)

    def remove_node_recurse(self, node):
        self.valid_node_in_tree(node)

        while node.first_child:
            FhTree.remove_node_recurse(self, node.first_child)

        if node.prev is None:
            return

        if node.prev.sib == node:
            node.prev.sib = node.sib

        else:
            node.prev.first_child = node.sib

        if node.sib:
            node.sib.prev = node.prev

        node.prev, node.first_child, node.sib, node.my_root = None, None, None, None

        self.m_size -= 1

    def size(self):
        return self.m_size


class FhSdTreeNode(FhTreeNode):
    def __init__(self, sib=None, first_child=None, prev=None, root=None, label=None, deleted=False):
        super().__init__(self, sib, first_child, prev, root)
        self.label = label
        self.deleted = deleted

    def __str__(self):
        return super().__str__(), "deleted: {}".format(self.deleted)


class FhSdTree(FhTree):
    def __init__(self):
        super().__init__()

    # def valid_node(self, node):

    # def valid_node_in_tree(self, node):

    def set_root(self, root):
        super().set_root(root)
        root.deleted = False

    def add_node(self, parent, child):
        self.valid_node_in_tree(parent)
        if parent.deleted:
            raise ValueError
        self.valid_node(child)

        child.sib = parent.first_child
        child.first_child = None
        child.prev = parent
        child.my_root = self.m_root
        child.deleted = False
        parent.first_child = child
        if child.sib:
            child.sib.prev = child

        self.m_size += 1

    def remove_node(self, node):
        self.valid_node_in_tree(node)
        node.deleted = True
        self.m_size -= 1
        if node == self.m_root:
            self.clear()

    # def __str__(self):

    def str_recurse(self, node, depth):
        if not node or node.deleted is False:
            return ""

        ret_str = self.BLANK * depth + str(node) + "\n"

        ret_str += self.str_recurse(node.first_child, depth + 1)
        ret_str += self.str_recurse(node.sib, depth)

        return ret_str

    def __repr__(self):
        return f"--- beginning of tree, size={self.size()} ---\n" + \
               self.repr_recurse(self.m_root, 0) + \
               "--- end of tree ---"

    def repr_recurse(self, node, depth):
        if not node:
            return ""

        ret_str = self.BLANK * depth + str(node) + "\n"
        if node.deleted:
            ret_str = ret_str + "(D)"
        ret_str += self.repr_recurse(node.first_child, depth + 1)
        # ret_str += self.repr_recurse(node.sib, depth)

        return ret_str

    def size(self):
        node = self.m_root

        return self.size_recurse(node)

    def size_recurse(self, node):
        self.valid_node_in_tree(node)

        count = 1

        while node.first_child:
            node = node.first_child
            count += 1

        if node.prev is None:
            return

        if node.prev.sib == node:
            node.prev.sib = node.sib
            count += 1
        else:
            node.prev.first_child = node.sib
            count += 1

        if node.sib:
            node.sib.prev = node.prev
            count += 1

        return count

    def size_physical(self):
        return self.m_size

    # def clear(self):

    def collect_garbage(self):
        node = self.m_root
        while node.deleted:
            self.collect_garbage_recurse(node)

    def collect_garbage_recurse(self, node):
        if node.deleted:
            self.remove_node(self.m_root)
            self.m_size -= 1
            node = node.prev
            self.collect_garbage_recurse(node)


class FhSdDataTreeNode(FhSdTreeNode):
    def __init__(self, data, sib=None, first_child=None, prev=None, root=None):
        super().__init__(sib, first_child, prev, root)
        self.data = data

    def __str__(self):
        return str(self.data)


class FhSdDataTree(FhSdTree):
    def __init__(self, data_type):
        super().__init__()
        if not isinstance(data_type, type):
            raise TypeError(f"data_type is {data_type}, not a type")
        self.data_type = data_type

    def __str__(self):
        return f"--- beginning of tree, size={self.size()} ---\n" + \
               self.str_recurse(self.m_root, 0) + \
               "--- end of tree ---"

    def str_recurse(self, node, depth):
        if not node:
            return ""

        ret_str = self.BLANK * depth + str(node) + "\n"

        ret_str += self.str_recurse(node.first_child, depth + 1)
        # ret_str += self.str_recurse(node.sib, depth)

        return ret_str

    def valid_data(self, data):
        if not isinstance(data, self.data_type):
            raise TypeError(f"data should be type {self.data_type}")

    def set_root_data(self, data):
        self.valid_data(data)
        self.set_root(FhSdDataTreeNode(data))

    def find(self, data):
        return self.find_recurse2(data, self.m_root)

    def find_recurse(self, data, node):
        if not node:
            return None

        if node.data == data and node.deleted is False:
            return node

        result = self.find_recurse(data, node.first_child)
        if result:
            return result
        else:
            return self.find_recurse(data, node.sib)

    def find_recurse2(self, data, node):
        if not node:
            return None

        if node.deleted and node.data == node.my_root:
            return None

        if node.data == data and node.deleted is False:
            return node

        child = node.first_child
        while child:
            result = self.find_recurse2(data, child)
            if result and result.deleted is False:
                return result
            child = child.sib

        return None

    def add_data(self, parent_data, data):
        self.valid_data(data)
        parent_node = self.find(parent_data)
        if parent_node:
            self.add_node(parent_node, FhSdDataTreeNode(data))
        else:
            raise KeyError(f"{parent_data} not found in tree for addition")

    def remove_data(self, data):
        node = self.find(data)
        if node:
            self.remove_node(node)
        else:
            raise KeyError(f"{data} not found in tree for removal")

    def traverse(self, func, result=None):
        return self.traverse_recurse(self.m_root, func, 0, result)

    def traverse_recurse(self, node, func, depth, result):
        if not node or node.deleted:
            return result

        result = func(node.data, depth, result)

        result = self.traverse_recurse(node.first_child, func, depth + 1, result)
        # result = self.traverse_recurse(node.sib, func, depth, result)

        return result


def fh_data_tree_test():
    tree = FhSdDataTree(int)
    tree.set_root_data(0)
    print(tree)

    tree.add_data(0, 3)
    tree.add_data(0, 2)
    tree.add_data(0, 1)

    tree.add_data(1, 5)
    tree.add_data(1, 4)

    tree.add_data(5, 9)
    tree.add_data(5, 8)
    tree.add_data(5, 7)
    tree.add_data(5, 6)
    print("whole tree", tree, sep="\n")

    # # removal
    tree.remove_data(2)
    print("after removing 2", tree, sep="\n")
    #
    tree.remove_data(5)
    print("after removing 5", tree, sep="\n")

    # traversal
    tree.traverse(lambda data, depth, result: print("  " * depth + str(data)))
    print("sum of all nodes:", tree.traverse(lambda data, depth, result: result + data, 0))


def fh_tree_test():
    nodes = {}
    for l in string.ascii_lowercase:
        nodes[l] = FhTreeNode(label=l)
    [print(f"{v}") for v in nodes.values()]

    # set root
    tree = FhTree()
    tree.set_root(nodes["a"])

    # add nodes
    tree.add_node(nodes["a"], nodes["d"])
    tree.add_node(nodes["a"], nodes["c"])
    tree.add_node(nodes["a"], nodes["b"])
    tree.add_node(nodes["b"], nodes["h"])
    tree.add_node(nodes["b"], nodes["g"])
    tree.add_node(nodes["b"], nodes["f"])
    tree.add_node(nodes["b"], nodes["e"])
    tree.add_node(nodes["c"], nodes["k"])
    tree.add_node(nodes["c"], nodes["j"])
    tree.add_node(nodes["c"], nodes["i"])
    tree.add_node(nodes["e"], nodes["l"])
    tree.add_node(nodes["g"], nodes["n"])
    tree.add_node(nodes["g"], nodes["m"])
    print("whole tree", tree, sep="\n")

    # removal
    tree.remove_node(nodes["b"])
    print("after removing b", tree, sep="\n")

    tree.remove_node(nodes["l"])
    print("after removing l", tree, sep="\n")
    tree.remove_node(nodes["j"])
    print("after removing j", tree, sep="\n")
    tree.remove_node(nodes["c"])
    print("after removing c", tree, sep="\n")
    tree.remove_node(nodes["b"])
    print("after removing b", tree, sep="\n")

    tree.remove_node(nodes["a"])
    print("after removing a", tree)


if __name__ == '__main__':
    fh_tree_test()
    fh_data_tree_test()
