import math
from re import compile as _re_compile
from copy import deepcopy

class MathItem(object):
    def __init__(self, data):
        self._data = data
        self._before = None
        self._afters = []

    @property
    def data(self):
        return self._data

    @property
    def before(self):
        return self._before

    def _set_before(self, before):
        self._before = before

    def append(self, after):
        self._afters.append(after)
        after._set_before(self)

    @staticmethod
    def isit(s):
        pass

    def __getitem__(self, ind):
        return self._afters[ind]

    def __repr__(self):
        return '{data}<{afters}>'.format(data=self._data, afters=self._afters)

    def __eq__(self, other):
        if not (isinstance(other, self.__class__) and self.data == other.data):
            return False

        return self._afters == other._afters

class Bracket(MathItem):
    def __init__(self):
        super(Bracket, self).__init__('()')

    @staticmethod
    def isit(self):
        """ not create bracket object """
        return None

class AbstractNumber(MathItem):
    pass

class Number(AbstractNumber):
    @staticmethod
    def isit(s):
        if s.isdigit():
            return Number(int(s))
        return None

class Variable(AbstractNumber):
    PATTERN = _re_compile(r'^[a-zA-Z]\d*$')
    @staticmethod
    def isit(s):
        m = Variable.PATTERN.search(s)
        if m:
            return Variable(s)
        else:
            return None

class Pi(AbstractNumber):
    def __init__(self):
        super(Pi, self).__init__('3.141592')

    @staticmethod
    def isit(s):
        if s == 'pi':
            return Pi()
        else:
            return None

class E(AbstractNumber):
    def __init__(self):
        super(E, self).__init__('2.718281')

    @staticmethod
    def isit(s):
        if s == 'e':
            return E()
        else:
            return None

ALL_NUMBERS = (Number, Variable, Pi, E)
def get_number(s):
    for num in ALL_NUMBERS:
        if num.isit(s):
            return num.isit(s)

    return None


class AbstractFunction(MathItem):
    def compute(self, x):
        pass

class Sin(AbstractFunction):
    def __init__(self):
        super(Sin, self).__init__('sin')

    @staticmethod
    def isit(s):
        if s == 'sin':
            return Sin()
        else:
            return None

    def compute(self, x):
        return math.sin(x)

class Cos(AbstractFunction):
    def __init__(self):
        super(Cos, self).__init__('cos')

    @staticmethod
    def isit(s):
        if s == 'cos':
            return Cos()
        else:
            return None

    def compute(self, x):
        return math.cos(x)

class Tan(AbstractFunction):
    def __init__(self):
        super(Tan, self).__init__('tan')

    @staticmethod
    def isit(s):
        if s == 'tan':
            return Tan()
        else:
            return None

    def compute(self, x):
        return math.tan(x)

ALL_FUNCTIONS = (Sin(), Cos(), Tan())
def get_function(s):
    for func in ALL_FUNCTIONS:
        if func.isit(s):
            return func
    else:
        return None

class AbstractOperand(MathItem):
    def compute(self, x, y):
        pass

    @property
    def priority(self):
        pass

class Plus(AbstractOperand):
    def __init__(self):
        super(Plus, self).__init__('+')

    @staticmethod
    def isit(s):
        if s == '+':
            return Plus()
        else:
            return None

    def compute(self, x, y):
        return x + y

    @property
    def priority(self):
        return 4

class Minus(AbstractOperand):
    def __init__(self):
        super(Minus, self).__init__('-')

    @staticmethod
    def isit(s):
        if s == '-':
            return Minus()
        else:
            return None

    def compute(self, x, y):
        return x - y

    @property
    def priority(self):
        return 4

class Product(AbstractOperand):
    def __init__(self):
        super(Product, self).__init__('*')

    @staticmethod
    def isit(s):
        if s == '*':
            return Product()
        else:
            return None

    @property
    def priority(self):
        return 6

    def compute(self, x, y):
        return x * y

class Divide(AbstractOperand):
    def __init__(self):
        super(Divide, self).__init__('/')

    def compute(self, x, y):
        return x / y

    @property
    def priority(self):
        return 6

    @staticmethod
    def isit(s):
        if s == '/':
            return Divide()
        else:
            return None

class Power(AbstractOperand):
    def __init__(self):
        super(Power, self).__init__('^')

    def compute(self, x, y):
        return x ** y

    @property
    def priority(self):
        return 8

    @staticmethod
    def isit(s):
        if s == '^':
            return Power()
        else:
            return None

ALL_OPERANDS = (Plus(), Minus(), Product(), Divide(), Power())
def get_operand(s):
    for ope in ALL_OPERANDS:
        if ope.isit(s):
            return deepcopy(ope)

    return None

def get_mathitem(s):
    num_obj = get_number(s)
    if num_obj:
        return num_obj

    func_obj = get_function(s)
    if func_obj:
        return func_obj

    ope_obj = get_operand(s)
    if ope_obj:
        return ope_obj

    return None

def _parse_from_str(s):
    # case: s is just one mathitem.
    mathitem = get_mathitem(s)
    if mathitem is not None:
        return mathitem

    # case: (mathitem1 mathitem2 ... ) format
    lv = 0
    for i, c in enumerate(s):
        if c == '(':
            lv += 1
        elif c == ')':
            lv -= 1
        if i != len(s) -1 and lv == 0:
            break
    else:
        math = Bracket()
        math.append(_parse_from_str(s[1:-1]))
        return math

    # case: mathobj op mathobj ... format
    lv = 0
    opes = []   # list of (ope, ope_index)
    for i, c in enumerate(s):
        if c == '(':
            lv += 1
        elif c == ')':
            lv -= 1
        elif lv == 0 and get_operand(c) is not None:
            ope = get_operand(c)
            opes.append((ope, i))
    if opes:
        ope, ope_index = min(opes, key=lambda ope_a: ope_a[0].priority)
        math = ope
        left = _parse_from_str(s[:ope_index])
        right = _parse_from_str(s[ope_index + 1:])
        math.append(left)
        math.append(right)
        return math

    # case: s is func(arg) format
    arg_start_index = s.find('(')
    func = get_function(s[:arg_start_index])
    if arg_start_index != -1 and s.endswith(')') and func:
        math = func
        math1 = Bracket()
        math2 = _parse_from_str(s[arg_start_index + 1: -1])
        math.append(math1)
        math1.append(math2)
        return math

def parse_from_str(s):
    dummies = (' ', '\t', '\r')
    for dummy in dummies:
        s = s.replace(dummy, '')
    return _parse_from_str(s)
