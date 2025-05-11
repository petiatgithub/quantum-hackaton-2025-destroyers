from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import CRZGate
import numpy as np
from qiskit.converters import circuit_to_dag

# Circuit implementing the QFT.
qc = QuantumCircuit(8)
for i in range(8):
    qc.h(i)
    for j in range(i + 1, 8):
        qc.crz(np.pi / (2**(j - i)), j,  i)
for i in range(3):
    qc.cx(i, 7 - i)
    qc.cx(7 - i, i)
    qc.cx(i, 7 - i)

# Transpile into the native gate set.
basis_gates = ['rxx', 'rx', 'ry']
transpiled_qc = transpile(qc, basis_gates=basis_gates, optimization_level=3, approximation_degree=1.0)
# print(transpiled_qc.depth())

dag = circuit_to_dag(transpiled_qc)

# Each layer is a list of gates that happen at a specific time step.
layers = []
for i, layer in enumerate(dag.layers()):
    current_layer = []
    for op in layer["graph"].op_nodes():
        if op.name == "rx":
            gate = ("RX", op.params[0], op.qargs[0]._index)
        elif op.name == "ry":
            gate = ("RY", op.params[0], op.qargs[0]._index)
        else:
            gate = ("MS", op.params[0], (op.qargs[0]._index, op.qargs[1]._index))
        current_layer.append(gate)
    layers.append(current_layer)
    # print(str(current_layer) + ",")
# print(layers)

print(transpiled_qc.draw(output='text'))
