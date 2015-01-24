from sys import path
path.append('src')
from formula import MathItem
from unittest import TestCase

class MathItemTest(TestCase):
    def mathitem_create_test(self):
        math = MathItem('data')

    def mathitem_set_before_test(self):
        math = MathItem('1')
        math._set_before(MathItem('2'))
        assert(math.before == MathItem('2'))

    def mathitem_append_test(self):
        math0 = MathItem('0')
        math1 = MathItem('1')
        math0.append(math1)
        math0[0] == math1
        assert(math1.before == math0)

    def mathitem_eq_test1(self):
        assert(MathItem(2) == MathItem(2))

    def mathitem_eq_test2(self):
        math1 = MathItem(2)
        math2 = MathItem(3)
        print(math1._data != math2._data)
        assert(MathItem(2) != MathItem(3))
