from assignment08 import *
import unittest


class DictionaryTest(unittest.TestCase):
    def test_dictionary(self):
        # test removal of oldest entry from cache
        dic_1 = Dictionary(2)
        dic_1.search('ace')
        dic_1.search('ace')
        dic_1.search('bird')
        dic_1.search('bird')
        dic_1.search('python')
        expected2 = dic_1.dic_cache.remove_oldest()
        self.assertTrue(expected2)

        # test that removal from cache ensures reaching from local
        dic_1 = Dictionary(2)
        a = dic_1.search('ace')
        dic_1.search('ace')
        dic_1.search('bird')
        dic_1.search('bird')
        dic_1.search('python')
        dic_1.dic_cache.remove_oldest()
        b = dic_1.search('ace')
        self.assertEqual(a, b)

        # testing that KeyError is raised if local dic does not contain search query
        dic_2 = Dictionary(1)
        with self.assertRaises(KeyError):
            dic_2.search('aces')

        # testing that capacity of cache is properly raising error
        with self.assertRaises(ValueError):
            dic_3 = Dictionary(0)

if __name__ == '__main__':
    unittest.main()