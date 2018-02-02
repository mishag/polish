import unittest
import math

from polish import eval_expr


class TestPolishCalculator(unittest.TestCase):

    def test_eval(self):
        res = eval_expr("3 5 * 2 + 7 -")
        self.assertEqual(res, 10)
        res = eval_expr("3 5 10 + *")
        self.assertEqual(res, 45)

    def test_assignment(self):
        res = eval_expr("x 3 =")
        self.assertEqual(res, 3)
        res = eval_expr("x")
        self.assertEqual(res, 3)

    def test_constants(self):
        self.assertEqual(eval_expr("pi"), math.pi)
        self.assertEqual(eval_expr("e"), math.exp(1))
        self.assertEqual(eval_expr("1"), 1)

    def test_trig(self):
        self.assertAlmostEqual(eval_expr("1 pi sin +"), 1)
        self.assertAlmostEqual(eval_expr("pi cos 8 *"), -8)
        self.assertAlmostEqual(eval_expr("pi 4 / tan"), 1)

    def test_cond(self):
        self.assertEqual(eval_expr("0 1 2 ?"), 2)
        self.assertEqual(eval_expr("1 1 2 ?"), 1)
        self.assertEqual(eval_expr("1 1 Y ?"), 1)
        self.assertEqual(eval_expr("0 Y 1 ?"), 1)
