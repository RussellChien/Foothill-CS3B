import unittest
from collections import namedtuple

from assignment09 import *


class FhSdTreeTest(unittest.TestCase):
    def setUp(self):
        self.tree = FhSdTree()

        # self.nodes has attributes a, b, c, ...  so self.nodes.a, self.nodes.b, self.nodes.c, ...
        self.nodes = namedtuple("nodes", list(string.ascii_lowercase)) \
            (*[FhSdTreeNode(label=l) for l in string.ascii_lowercase])

        self.tree.set_root(self.nodes.a)
        self.tree.add_node(self.nodes.a, self.nodes.d)
        self.tree.add_node(self.nodes.a, self.nodes.c)
        self.tree.add_node(self.nodes.a, self.nodes.b)

        self.tree.add_node(self.nodes.b, self.nodes.f)
        self.tree.add_node(self.nodes.b, self.nodes.e)

        print(self.tree)

    def testSetRoot(self):
        # Check the root
        self.assertIs(self.nodes.a, self.tree.m_root)
        self.assertFalse(self.nodes.a.deleted)

    def testAddNode(self):
        # Check all the forward references
        self.assertIs(self.nodes.b, self.nodes.a.first_child)
        self.assertIs(self.nodes.c, self.nodes.b.sib)
        self.assertIs(self.nodes.d, self.nodes.c.sib)

        self.assertIs(self.nodes.e, self.nodes.b.first_child)
        self.assertIs(self.nodes.f, self.nodes.e.sib)

    def testSize(self):
        # Check size
        self.assertEqual(6, self.tree.size())
        self.assertEqual(6, self.tree.size_physical())

    def testRemoveRootNode(self):
        self.tree.remove_node(self.nodes.a)
        self.assertEqual(0, self.tree.size(), "size should be 0 when root node is removed")
        self.assertEqual(0, self.tree.size_physical(), "size should be 0 when root node is removed")

    def testDeletedAttribute(self):
        self.assertFalse(self.nodes.b.deleted, "deleted should be false by default")
        self.tree.remove_node(self.nodes.b)
        self.assertTrue(self.nodes.b.deleted, "deleted should be true when removed")

    def testRemoveNodeFirstSibling(self):
        self.tree.remove_node(self.nodes.e)
        self.assertEqual(5, self.tree.size())
        self.assertEqual(6, self.tree.size_physical())

    def testRemoveNodeMiddleOfSiblings(self):
        self.tree.remove_node(self.nodes.c)
        self.assertEqual(5, self.tree.size())
        self.assertEqual(6, self.tree.size_physical())

    def testRemoveNodeLastSibling(self):
        self.tree.remove_node(self.nodes.f)
        self.assertEqual(5, self.tree.size())
        self.assertEqual(6, self.tree.size_physical())


class FhSdDataTreeTest(unittest.TestCase):
    def setUp(self):
        self.tree = FhSdDataTree(str)
        self.tree.set_root_data("vertebrate")
        self.tree.add_data("vertebrate", "reptiles")
        self.tree.add_data("vertebrate", "fish")
        self.tree.add_data("vertebrate", "mammals")
        self.tree.add_data("reptiles", "snake")
        self.tree.add_data("fish", "shark")
        self.tree.add_data("fish", "tuna")
        self.tree.add_data("mammals", "cow")
        self.tree.add_data("mammals", "lion")
        self.tree.add_data("mammals", "tiger")

        # add these if you want more complicated tests
        #
        # tree.add_data("vertebrate", "amphibians")
        # tree.add_data("vertebrate", "birds")
        #
        # tree.add_data("amphibians", "frog")
        # tree.add_data("amphibians", "newt")
        #
        # tree.add_data("birds", "owl")
        # tree.add_data("birds", "seagull")
        # tree.add_data("birds", "swan")
        #
        # tree.add_data("owl", "barn owl")
        # tree.add_data("owl", "snowy owl")
        # tree.add_data("owl", "tarny owl")

    def testSize(self):
        print(self.tree)

        self.assertEqual(10, self.tree.size())
        self.assertEqual(10, self.tree.size_physical())

    def testFind(self):
        self.assertIsNotNone(self.tree.find("lion"), "should find lion")
        self.assertIsNone(self.tree.find("dragon"), "should not have dragon")

    def testRemoveData(self):
        self.tree.remove_data("lion")
        print("tree after removing lion:", str(self.tree), sep="\n")
        self.assertIsNone(self.tree.find("lion"), "should not find lion after removing it")

        self.tree.remove_data("mammals")
        self.assertIsNone(self.tree.find("mammals"), "should not find mammals after removing mammals")
        self.assertIsNone(self.tree.find("tiger"), "should not find tiger after removing mammals")
        self.assertIsNone(self.tree.find("lion"), "should not find lion after removing mammals")
        self.assertIsNone(self.tree.find("cow"), "should not find cow after removing mammals")

        print("tree after removing mammals:", str(self.tree), sep="\n")
        print("physical tree after removing mammals:", repr(self.tree), sep="\n")
        self.assertEqual(6, self.tree.size(), "size should be 6 after removing mammals")
        self.assertEqual(10, self.tree.size_physical(), "physical size should be 10 after removing mammals")

    def testCollectGarbage(self):
        self.tree.remove_data("lion")
        self.tree.remove_data("mammals")

        self.tree.collect_garbage()
        print("tree after garbage collection:", str(self.tree), sep="\n")
        print("physical tree after garbage collection:", repr(self.tree), sep="\n")

        self.assertEqual(6, self.tree.size(), "size should be 6 after garbage collection")
        self.assertEqual(6, self.tree.size(), "physical size should be 6 after garbage collection")
