import unittest
import eval
import input

class TestEvalMethod(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.n, self.e, self.g = input.read_local("./test.graph")
        
    def test_single_cut(self):
        self.assertEqual(eval.single_cut(self.g,[],[1]), 0, "Cut should be 0")
        self.assertEqual(eval.single_cut(self.g,[1],[2,3]), 2, "Cut should be 2")
        self.assertEqual(eval.single_cut(self.g,[1,2,3,5,6,7],[4]), 1, "Cut should be 3")
        
    def test_cut(self):
        self.assertEqual(eval.cut(self.g,[[1,2,3,5,6,7],[4]]), 1, "Cut should be 1 (sole link btw 6 and 4)")
        self.assertEqual(eval.cut(self.g,[[1,2],[3,5,6,7],[4]]), 4, "Cut should be 3+1=4")
        self.assertEqual(eval.cut(self.g,[[1],[2],[3],[4],[5],[6],[7]]), 10, "Cut should be equal to nb of edges (10)")
if __name__ == '__main__':
    unittest.main()