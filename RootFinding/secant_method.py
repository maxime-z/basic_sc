"""Demonstration of the secant method for root finding"""
import numpy as np


def f(x):
    """Function whose root to found"""
    return 10 - x ** 2


class SecantMethod:
    """Secant method for scalar valued function"""

    def __init__(self, func, root_brackets):
        self.func = func

        assert len(root_brackets) == 2, "root brackets should have 2 elements!"
        a = root_brackets[0]
        b = root_brackets[1]
        fa = func(a)
        fb = func(b)

        assert (fa < 0) ^ (fb < 0), "function should not have the same sign!"

        # object attribute 'a' always has a negative function value
        if fa < 0 and fb > 0:
            self.a = a
            self.b = b
        else:
            self.a = b
            self.b = a

    def solve(self, converge_criterion):
        # TODO: error estimation.
        ai = self.a
        while not np.isclose(self.func(ai), 0, atol=converge_criterion):
            da = -self.func(ai) * (self.b - ai) / (self.func(self.b) - self.func(ai))
            ai += da

        return ai


if __name__ == '__main__':
    sm = SecantMethod(f, [2, 4])
    print(sm.solve(1e-5))
