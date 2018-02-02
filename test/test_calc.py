import unittest
from polish import eval_expr


class TestPolishCalculator(unittest.TestCase):

    def test_eval(self):
        res = eval_expr("3 5 * 2 + 7 -")
        self.assertEqual(res, 10)
