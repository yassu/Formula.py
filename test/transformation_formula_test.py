from sys import path
path.append('src')
from formula import Plus, Number
from transformation_formula import symplify

def symplify_test1():
    math = Plus()
    math.append(Number(1))
    math.append(Number(2))
    assert(symplify(math) == Number(3))
