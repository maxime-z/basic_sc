"""Module for a demo implementation of dual number reverse auto-diff"""

import numpy as np


class Operator(object):

    def __call__(self, *args):
        pass

    def partial_derivation(self, n: int):
        pass

    def derivate(self, *args):
        pass


class Product(Operator):

    def __call__(self, a, b):
        return a * b

    def derivate(self, a, b, a_, b_):
        return a_ * b + a * b_


class Log(Operator):

    def __call__(self, a):
        return np.log(a)

    def derivate(self, a, a_):
        return 1 / a * a_


class Sin(Operator):
    def __call__(self, a):
        return np.sin(a)

    def derivate(self, a, a_):
        return np.cos(a) * a_


class Minus(Operator):
    def __call__(self, a, b):
        return a - b

    def derivate(self, a, b, a_, b_):
        return a_ - b_


class Plus(Operator):
    def __call__(self, a, b):
        return a + b

    def derivate(self, a, b, a_, b_):
        return a_ + b_


class Assignment(Operator):
    def __init__(self, val):
        self.value = val

    def __call__(self):
        return self.value

    def derivate(self):
        return 0


class Node(object):
    def __init__(self, output=None, op: Operator = None):
        # inputs should be list of nodes
        self.inputs = []
        self.op = op
        self.value = 0
        self.grad = 0
        self.adjoint = 0

    def _parameters(self):
        return [in_node.value for in_node in self.inputs]

    def _diff_parameters(self):
        return [in_node.grad for in_node in self.inputs]

    def add_input(self, node):
        self.inputs.append(node)

    def evaluate(self):
        """Evaluate the value of the node"""
        self.value = self.op(*self._parameters())

    def diff(self):
        self.grad = self.op.derivate(*(self._parameters() + self._diff_parameters()))

    def diff_ext(self, *args):
        return self.op.derivate(*args)


class Graph(object):
    def __init__(self):
        self.nodes = []

    def execute(self, node):
        """Execution by DFS traversal"""
        if len(node.inputs) is not 0:
            for n in node.inputs:
                self.execute(n)
        node.evaluate()

    def forward_gradient(self, node, varying_node):
        if len(node.inputs) is not 0:
            for n in node.inputs:
                self.forward_gradient(n, varying_node)

        node.evaluate()
        node.diff()

        if node is varying_node:
            node.grad = 1


    """Reverse mode of auto differentiation"""
    def reverse_gradient(self, node):
        # forward execution
        self.execute(node)

        # reverse mode for differentiation
        node.adjoint = 1

        # queue FIFO
        queue = list()
        queue.append(node)

        while queue:
            s = queue.pop(0)
            self.compute_input_ajoint(s)
            for n in s.inputs:
                queue.append(n)

    def compute_input_ajoint(self, node):

        if len(node.inputs) is 0:
            return

        for n in node.inputs:
            parameters = node._parameters()

            for ni in node.inputs:
                if ni is n:
                    parameters.append(1.)
                else:
                    parameters.append(0.)

            n.adjoint += node.adjoint * node.diff_ext(*parameters)
