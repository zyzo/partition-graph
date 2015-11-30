import unittest
import eval
import input


class TestEvalMethod(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n, cls.e, cls.g = input.read_local("./test.graph")

    def test_single_cut(self):
        self.assertEqual(eval.single_cut(self.g,[],[1]), 0)
        self.assertEqual(eval.single_cut(self.g,[1],[2,3]), 2)
        self.assertEqual(eval.single_cut(self.g,[1,2,3,5,6,7],[4]), 1)
        
    def test_cut(self):
        self.assertEqual(eval.cut(self.g,[[1,2,3,5,6,7],[4]]), 1)
        self.assertEqual(eval.cut(self.g,[[1,2],[3,5,6,7],[4]]), 4)
        self.assertEqual(eval.cut(self.g,[[1],[2],[3],[4],[5],[6],[7]]), 10)
        self.assertEqual(eval.cut(self.g,[[3,1,2],[6,4,5,7]]), 3)

    def test_weight(self):
        self.assertEqual(eval.weight(self.g,[1]), 0)
        self.assertEqual(eval.weight(self.g,[1,2]), 1)
        self.assertEqual(eval.weight(self.g,[1,2,3]), 3)
        self.assertEqual(eval.weight(self.g,[1,2,3,4,5,6,7]), 10)

    def test_ratio(self):
        self.assertEqual(eval.ratio(self.g,[[1,2,3,5,7],[4,6]]), 5)
        # self.assertEqual(eval.ratio(self.g,[[1,2],[3,5,6,7],[4]]), 4)
        # self.assertEqual(eval.ratio(self.g,[[1],[2],[3],[4],[5],[6],[7]]), 10)
if __name__ == '__main__':
    unittest.main()