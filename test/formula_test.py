from sys import path
path.append('src')
from formula import (
        MathItem,
        Bracket,
        AbstractNumber, Number, Variable, Pi, E, get_number,
        AbstractFunction, Sin, Cos, Tan, get_function,
            FunctionDataLengthException,
        AbstractOperand, Plus, Minus, Product, Divide, Power, get_operand,
            OperandDataLengthException,
        get_mathitem,
    )
from unittest import TestCase
from nose.tools import raises
import math


class MathItemTest(TestCase):
    def create_test(self):
        math = MathItem('123')

    def data_test(self):
        math = MathItem(1)
        assert(math.data == 1)

    def before_test(self):
        math = MathItem(1)
        math2 = MathItem(2)
        math2._before = math
        assert(math2.before == math)

    def after_test(self):
        math = MathItem(1)
        math2 = MathItem(2)
        math._afters.append(math2)
        assert(math[0] == math2)

    def append_test(self):
        math = MathItem(1)
        math2 = MathItem(2)
        math.append(math2)
        assert(math[0] == math2)
        assert(math2.before == math)

    def repr_test(self):
        math = MathItem(Sin())
        math10 = MathItem(Cos())
        math11 = MathItem(Tan())
        math.append(math10)
        math.append(math11)

        assert(repr(math) == 'sin<[]><[cos<[]><[]>, tan<[]><[]>]>')

    def eq_test(self):
        math1 = MathItem(2)
        math2 = MathItem(2)
        assert(math1 == math2)

    def eq_test2(self):
        math1 = MathItem(2)
        math2 = MathItem(3)
        assert(math1 != math2)

    def eq_test3(self):
        math01 = MathItem(2)
        math02 = MathItem(3)
        math01.append(math02)

        math11 = MathItem(2)
        math12 = MathItem(1)

        assert(math01 != math11)

class BracketItemTest(TestCase):
    def create_test(self):
        Bracket()

    def isit_test1(self):
        assert(Bracket.isit('()') is None)


class NumberTest(TestCase):
    def instance_test(self):
        num = Number(1)
        isinstance(num, AbstractNumber)
        isinstance(num, MathItem)

    def isit_test1(self):
        assert(Number.isit('12') == Number(12))

    def isit_test2(self):
        assert(Number.isit('ab') is None)

class VariableTest(TestCase):
    def instance_test(self):
        var = Variable('t1')
        isinstance(var, AbstractNumber)
        isinstance(var, MathItem)

    def isit_test(self):
        assert(Variable.isit('t1') == Variable('t1'))

class PiTest(TestCase):
    def instance_test(self):
        pi = Pi()
        assert(isinstance(pi, AbstractNumber))

    def isit_test1(self):
        assert(Pi.isit('pi') == Pi())

    def isit_test2(self):
        assert(Pi.isit('ab') is None)

class ETest(TestCase):
    def instance_test(self):
        e = E()
        assert(isinstance(e, AbstractNumber))

    def isit_test1(self):
        assert(E.isit('e') == E())

    def isit_test2(self):
        assert(E.isit('E') is None)

def get_number_test1():
    assert(get_number('pi') == Pi())

def get_number_test2():
    assert(get_number('12') == Number(12))

class AbstractFunctionTest(TestCase):
    @raises(FunctionDataLengthException)
    def create_exception_test(self):
        AbstractFunction('s')

class SinTest(TestCase):
    def create_test(self):
        sin = Sin()
        assert(isinstance(sin, AbstractFunction))

    def compute_test(self):
        assert(math.sin(math.pi/10) == Sin().compute(math.pi/10))

    def isit_test1(self):
        assert(Sin.isit('sin') == Sin())

    def isit_test2(self):
        assert(Sin.isit('cos') is None)

class CosTest(TestCase):
    def create_test(self):
        cos = Cos()
        assert(isinstance(cos, AbstractFunction))

    def compute_test(self):
        assert(Cos().compute(math.pi/10) == math.cos(math.pi/10))

    def isit_test1(self):
        assert(Cos.isit('cos') == Cos())

    def isit_test2(self):
        assert(Cos.isit('sin') is None)

class TanTest(TestCase):
    def create_test(self):
        tan = Tan()
        assert(isinstance(tan, AbstractFunction))

    def compute_test(self):
        assert(Tan().compute(math.pi/10) == math.tan(math.pi/10))

    def isit_test1(self):
        assert(Tan.isit('tan') == Tan())

    def isit_test2(self):
        assert(Tan.isit('cos') is None)

def get_function_test1():
    assert(get_function('sin') == Sin())

def get_function_test2():
    assert(get_function('cos') == Cos())

def get_function_test3():
    assert(get_function('$$') is None)

class AbstractOperandTest(TestCase):
    @raises(OperandDataLengthException)
    def create_exception_test(self):
        AbstractOperand('**')

class PlusTest(TestCase):
    def create_test(self):
        p = Plus()
        isinstance(p, AbstractOperand)

    def isit_test1(self):
        assert(Plus.isit('+') == Plus())

    def isit_test2(self):
        assert(Plus.isit('+12') is None)

    def compute_test(self):
        assert(Plus().compute(123, 144) == 123 + 144)

    def priority_test(self):
        assert(Plus().priority == 4)

class MinusTest(TestCase):
    def create_test(self):
        m = Minus()
        isinstance(m, AbstractOperand)

    def isit_test1(self):
        assert(Minus.isit('-') == Minus())

    def isit_test2(self):
        Minus.isit('$' is None)

    def compute_test(self):
        assert(Minus().compute(154, 199) == 154 - 199)

    def priority_test(self):
        assert(Minus().priority == 4)


class ProductTest(TestCase):
    def create_test(self):
        p = Product()
        assert(isinstance(p, AbstractOperand))

    def isit_test1(self):
        assert(Product.isit('*') == Product())

    def isit_test2(self):
        assert(Product.isit('+a') is None)

    def compute_test(self):
        assert(Product().compute(12, 34) == 12 * 34)

    def priority_test(self):
        assert(Product().priority == 6)

class DivideTest(TestCase):
    def create_test(self):
        d = Divide()
        assert(isinstance(d, AbstractOperand))

    def isit_test1(self):
        assert(Divide().isit('/') == Divide())

    def isit_test2(self):
        assert(Divide().isit('&') is None)

    def compute_test(self):
        assert(Divide().compute(179, 122) == 179/122)

    def priority_test(self):
        assert(Divide().priority == 6)

class PowerTest(TestCase):
    def create_test(self):
        p = Power()
        assert(isinstance(p, AbstractOperand))

    def isit_test1(self):
        assert(Power.isit('^') == Power())

    def isit_test2(self):
        assert(Power.isit('*') is None)

    def compute_test(self):
        assert(11**13 == Power().compute(11, 13))

    def priority_test(self):
        assert(Power().priority == 8)

def get_operand_test1():
    assert(get_operand('+') == Plus())

def get_operand_test2():
    assert(get_operand('-') == Minus())

def get_mathitem_test1():
    assert(get_mathitem('+') == Plus())

def get_mathitem_test2():
    assert(get_mathitem('12') == Number(12))

def get_mathitem_test3():
    assert(get_mathitem('$') is None)

# def parse_from_str_test1():
#     assert(parse_from_str('1') == Number(1))
#
# def parse_from_str_test2():
#     math = Plus()
#     math.append(Number(1))
#     math.append(Number(2))
#     assert(parse_from_str('1 + 2') == math)
#
# def parse_from_str_test3():
#     math = Plus()
#     math.append(Number(1))
#     math.append(Number(2))
#     _math = parse_from_str('(1) + (2)')
#     print(list(math))
#     assert(parse_from_str('(1) + (2)') == math)
#
# def parse_from_str_test4():
#     math = Plus()
#     math.append(Number(1))
#     math.append(Number(2))
#     assert(parse_from_str('(1 + 2)') == math)
#
# def parse_from_str_test5():
#     math00 = Power()
#     math10 = Plus()
#     math11 = Number(5)
#     math21 = Number(1)
#     math22 = Number(2)
#
#     math00.append(math10)
#     math00.append(math11)
#     math10.append(math21)
#     math10.append(math22)
#     assert(parse_from_str('(1 + 2)^3') == math00)
