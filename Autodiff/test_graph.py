import unittest
from Autodiff.computation_graph import *


class GraphTest(unittest.TestCase):

    def setUp(self) -> None:
        v5 = Node(op=Minus())
        v4 = Node(op=Plus())
        v3 = Node(op=Sin())
        v2 = Node(op=Product())
        v1 = Node(op=Log())
        v0 = Node(op=Assignment(52))
        v_1 = Node(op=Assignment(21.3))

        v5.add_input(v4)
        v5.add_input(v3)

        v4.add_input(v1)
        v4.add_input(v2)

        v3.add_input(v0)

        v2.add_input(v_1)
        v2.add_input(v0)

        v1.add_input(v_1)
        self.nodes = [v_1, v0, v1, v2, v3, v4, v5]

    def test_evaluation(self):
        graph = Graph()
        graph.execute(self.nodes[-1])
        inputs = [self.nodes[0].value, self.nodes[1].value]

        self.ref_func = lambda x1, x2: np.log(x1) + x1 * x2 - np.sin(x2)
        self.assertAlmostEqual(self.nodes[-1].value, self.ref_func(*inputs))

    def test_gradient(self):
        graph = Graph()
        # derivation with respect to v_1
        graph.forward_gradient(self.nodes[-1], self.nodes[0])
        inputs = [self.nodes[0].value, self.nodes[1].value]

        self.ref_func = lambda x1, x2: np.log(x1) + x1 * x2 - np.sin(x2)
        self.grad1 = lambda x1, x2: 1 / x1 + x2

        self.assertAlmostEqual(self.nodes[-1].value, self.ref_func(*inputs))
        self.assertAlmostEqual(self.nodes[-1].grad, self.grad1(*inputs))

        # derivation with respect to v0
        graph.forward_gradient(self.nodes[-1], self.nodes[1])
        self.grad2 = lambda x1, x2: x1 - np.cos(x2)
        self.assertAlmostEqual(self.nodes[-1].value, self.ref_func(*inputs))
        self.assertAlmostEqual(self.nodes[-1].grad, self.grad2(*inputs))

    def test_reverse_gradient(self):
        # reverse mode
        graph = Graph()
        graph.reverse_gradient(self.nodes[-1])

        inputs = [self.nodes[0].value, self.nodes[1].value]

        self.ref_func = lambda x1, x2: np.log(x1) + x1 * x2 - np.sin(x2)
        self.grad1 = lambda x1, x2: 1 / x1 + x2
        self.assertAlmostEqual(self.nodes[0].adjoint, self.grad1(*inputs))

        # derivation with respect to v0

        self.grad2 = lambda x1, x2: x1 - np.cos(x2)
        self.assertAlmostEqual(self.nodes[1].adjoint, self.grad2(*inputs))
