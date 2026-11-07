#!/usr/bin/env python3
"""Independent black-box micrograd contract checks. Run only in a disposable runner."""
from __future__ import annotations

import json
import math
import random
import sys
import unittest
from pathlib import Path


class MicrogradContract(unittest.TestCase):
    def test_scalar_arithmetic_and_backprop(self):
        from micrograd.engine import Value

        a, b = Value(-4.0), Value(2.0)
        c = a + b
        d = a * b + b ** 3
        c += c + 1
        c += 1 + c + (-a)
        d += d * 2 + (b + a).relu()
        d += 3 * d + (b - a).relu()
        e = c - d
        f = e ** 2
        g = f / 2.0
        g += 10.0 / f
        self.assertAlmostEqual(g.data, 24.7041, places=3)
        g.backward()
        self.assertAlmostEqual(a.grad, 138.8338, places=3)
        self.assertAlmostEqual(b.grad, 645.5773, places=3)

    def test_shared_nodes_accumulate_gradients(self):
        from micrograd.engine import Value

        x = Value(3.0)
        y = x * x + x
        y.backward()
        self.assertAlmostEqual(x.grad, 7.0)
        x = Value(2.0)
        y = x * x
        (y + y).backward()
        self.assertAlmostEqual(x.grad, 8.0)

    def test_numeric_reflected_operators(self):
        from micrograd.engine import Value

        x = Value(4.0)
        out = 10.0 / x + 2.0 * x - (9.0 - x)
        self.assertAlmostEqual(out.data, 5.5)
        out.backward()
        self.assertAlmostEqual(x.grad, -10.0 / 16.0 + 2.0 + 1.0)

    def test_relu_gradient_and_boundary(self):
        from micrograd.engine import Value

        for data, expected_y, expected_grad in (
            (-3.0, 0.0, 0.0), (0.0, 0.0, 0.0), (2.5, 2.5, 1.0)
        ):
            with self.subTest(data=data):
                x = Value(data)
                out = x.relu()
                self.assertAlmostEqual(out.data, expected_y)
                out.backward()
                self.assertAlmostEqual(x.grad, expected_grad)

    def test_finite_difference_gradient(self):
        from micrograd.engine import Value

        def f(x, y):
            return (x * y + 1.5) ** 3 + x / 2.5 - 2.0 / y

        x, y = Value(0.8), Value(-1.2)
        z = f(x, y)
        z.backward()
        h = 1e-6
        df_dx = (f(0.8 + h, -1.2) - f(0.8 - h, -1.2)) / (2 * h)
        df_dy = (f(0.8, -1.2 + h) - f(0.8, -1.2 - h)) / (2 * h)
        self.assertTrue(math.isclose(x.grad, df_dx, rel_tol=1e-5, abs_tol=1e-5))
        self.assertTrue(math.isclose(y.grad, df_dy, rel_tol=1e-5, abs_tol=1e-5))

    def test_neuron_parameter_count_and_forward(self):
        from micrograd.nn import Neuron

        random.seed(100)
        n = Neuron(2, nonlin=False)
        self.assertEqual(len(n.parameters()), 3)
        n.w[0].data, n.w[1].data, n.b.data = 2.0, -1.0, 0.5
        out = n([3.0, 1.0])
        self.assertAlmostEqual(out.data, 5.5)
        out.backward()
        self.assertAlmostEqual(n.w[0].grad, 3.0)
        self.assertAlmostEqual(n.w[1].grad, 1.0)
        self.assertAlmostEqual(n.b.grad, 1.0)
        n.zero_grad()
        self.assertTrue(all(p.grad == 0 for p in n.parameters()))

    def test_layer_output_shape(self):
        from micrograd.engine import Value
        from micrograd.nn import Layer

        random.seed(7)
        self.assertIsInstance(Layer(2, 1)([1.0, -2.0]), Value)
        result = Layer(2, 3)([1.0, -2.0])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(isinstance(x, Value) for x in result))

    def test_mlp_parameter_count(self):
        from micrograd.nn import MLP

        random.seed(7)
        network = MLP(3, [4, 4, 1])
        self.assertEqual(len(network.parameters()), 41)
        self.assertEqual(len({id(p) for p in network.parameters()}), 41)
        self.assertTrue(hasattr(network([1.0, 2.0, -1.0]), "backward"))

    def test_sgd_reduces_loss(self):
        from micrograd.nn import MLP

        random.seed(1)
        network = MLP(1, [1])
        xs = [-1.0, 0.0, 1.0]
        ys = [-1.5, 0.5, 2.5]

        def loss():
            return sum((network([x]) - y) ** 2 for x, y in zip(xs, ys))

        before = loss().data
        for _ in range(50):
            network.zero_grad()
            current = loss()
            current.backward()
            for p in network.parameters():
                p.data -= 0.05 * p.grad
        self.assertLess(loss().data, before * 0.05)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python grade.py WORKSPACE")
    workspace = Path(sys.argv[1]).resolve()
    if not workspace.is_dir():
        raise SystemExit(f"not a directory: {workspace}")
    sys.path.insert(0, str(workspace))
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MicrogradContract)
    total = suite.countTestCases()
    result = unittest.TestResult()
    suite.run(result)
    failures = result.failures + result.errors
    payload = {
        "passed": total - len(failures) - len(result.skipped),
        "total": total,
        "success": result.wasSuccessful() and not result.skipped,
        "failures": [
            {"test": str(case), "error": error.splitlines()[-1][:300]}
            for case, error in failures
        ],
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
