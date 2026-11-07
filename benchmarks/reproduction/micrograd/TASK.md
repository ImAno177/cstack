# Reproduce a tiny scalar automatic-differentiation library

Implement a self-contained Python 3 package named \`micrograd\` from this specification.
Do **not** fetch, inspect, clone, or copy a reference repository, implementation, or
external solution. You may use Python's standard library only.

## Required layout

- \`micrograd/__init__.py\`
- \`micrograd/engine.py\`, exporting \`Value\`
- \`micrograd/nn.py\`, exporting \`Module\`, \`Neuron\`, \`Layer\`, and \`MLP\`

## Value

\`Value(data)\` holds a scalar \`.data\` and an accumulated scalar \`.grad\`
(initially 0). Its arithmetic builds a directed acyclic graph so that
\`output.backward()\` computes derivatives of the output with respect to
every reachable \`Value\`, including shared operands.

Support \`+\`, \`-\`, \`*\`, \`/\`, unary \`-\`, numeric exponentiation
(\`**\` with an int/float exponent), reversed numeric operands
(e.g. \`2 + value\`, \`3 / value\`), and \`value.relu()\`.
ReLU returns max(0, data), with derivative zero at data <= 0.

Backpropagate with the chain rule in reverse topological order, **accumulating**
gradients from all paths. No tensors, PyTorch, NumPy, graph visualization,
or command-line interface are required.

## Neural-network layer

- \`Module.parameters()\`: empty list by default.
- \`Module.zero_grad()\`: reset all parameter gradients to zero.
- \`Neuron(nin, nonlin=True)\`: has \`nin\` scalar \`Value\` weights sampled
  uniformly from [-1, 1], a zero-valued \`Value\` bias, and a \`nonlin\` flag.
  Calling a neuron on a sequence of inputs returns the weighted sum with
  optional ReLU.
- \`Layer(nin, nout, **kwargs)\`: \`nout\` neurons. Calling it returns one
  \`Value\` when \`nout == 1\`, otherwise a list of \`Value\`s.
- \`MLP(nin, nouts)\`: feedforward layers with widths in \`nouts\`. Hidden
  layers use ReLU; the final layer is linear. Calling it returns the final
  layer output.
- \`parameters()\` for each neural component returns every trainable weight
  and bias exactly once; support gradient descent by mutating \`.data\`.

## Completion

Implement the package, run your own focused checks, and give a brief report.
Do not write to GitHub, install dependencies, or access the network.
