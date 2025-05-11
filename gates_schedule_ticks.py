from typing import List
from dataclasses import dataclass

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import CRZGate
import numpy as np
from qiskit.converters import circuit_to_dag

# Create a circuit with a CRZ gate
qc = QuantumCircuit(8)
for i in range(8):
    qc.h(i)
    for j in range(i + 1, 8):
        qc.crz(np.pi / (2**(j - i)), j,  i)
for i in range(3):
    qc.cx(i, 7 - i)
    qc.cx(7 - i, i)
    qc.cx(i, 7 - i)


basis_gates = ['rxx', 'rx', 'ry']
transpiled_qc = transpile(qc, basis_gates=basis_gates, optimization_level=3, approximation_degree=1.0)

# print(transpiled_qc.depth())

dag = circuit_to_dag(transpiled_qc)

layers = []
for i, layer in enumerate(dag.ticks()):
    print(f"Layer {i}:")
    current_layer = []
    for op in layer["graph"].op_nodes():
        if op.name == "rx":
            gate = ("RX", op.params[0], op.qargs[0]._index)
        elif op.name == "ry":
            gate = ("RY", op.params[0], op.qargs[0]._index)
        else:
            gate = ("MS", op.params[0], (op.qargs[0]._index, op.qargs[1]._index))
        #print(f"  {op.name} on {op.qargs} with params {op.params}")
        print(f"  {gate}")
        current_layer.append(gate)
    layers.append(current_layer)
#print(layers)
print(layers[0][0])
print(layers[0][0][0])
print(layers[0][0][1])

# Draw the transpiled circuit
# print(transpiled_qc.draw(output='text'))



layers_ticks = []

@dataclass
class Tick():

     gates = [None] * 8
     time = time = 0
     layer_type = None # 'D' or 'S'



class GatesScheduleTicks():

    def __init__(self):
        self.tick:Tick = None
        self.is_wire_free = None
        self.ticks: List[Tick] = []
        self.add_tick()


    def gen(self, gates_in):

        buttom_in = 0

        while buttom_in < len(gates_in):
            scan_in = buttom_in
            while scan_in < len(gates_in):
                # check iof adding gate is abelian
                if gates_in[scan_in][0] == 'RX' or gates_in[scan_in][0] == 'RY':
                    # check if gate is in single qbit gate tick
                    if (len(self.ticks) % 3 != 0) and self.is_wire_free[gates_in[scan_in][2]]:
                        self.tick.gates[gates_in[scan_in][2]] = gates_in[scan_in]
                        buttom_in += 1
                    self.is_wire_free[gates_in[scan_in][2]] = False
                elif gates_in[scan_in][0] == 'MS':
                    # check if gate is in two qbit gate tick
                    if (len(self.ticks) % 3 == 0) and self.is_wire_free[gates_in[scan_in][2][0]] and self.is_wire_free[gates_in[scan_in][2][1]]:
                        self.tick.gates[gates_in[scan_in][2][0]] = gates_in[scan_in]
                        # only add once
                        buttom_in += 1
                    self.is_wire_free[gates_in[scan_in][2][0]] = False
                    self.is_wire_free[gates_in[scan_in][2][1]] = False
                else:
                    raise ValueError("Unexpected gate tyep" + gates_in[scan_in][0] + ".")
                scan_in += 1

            self.add_tick()

    def add_tick(self) -> Tick:

        self.is_wire_free = [True] * 8

        if self.tick is not None:
            wire = 0
            while wire < len(self.is_wire_free):
                if self.tick.gates[wire] is not None:
                    if self.tick.gates[wire][0] == 'MS':
                        self.is_wire_free[self.tick.gates[wire][2][0]] = False
                        self.is_wire_free[self.tick.gates[wire][2][1]] = False

        self.tick = Tick()
        self.ticks.append(self.tick)

gates = [gate for layer in layers for gate in layer]

# print(layers)
# print(gates)

tmp = GatesScheduleTicks()
tmp.gen(gates)
print(tmp.ticks)
