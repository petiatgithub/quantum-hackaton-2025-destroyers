import pennylane as qml
import numpy as np

n_qubits = 8

dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def circuit():
    for i in range(n_qubits):
        qml.Hadamard(wires=i)
        for j in range(i+1, n_qubits):
            angle = np.pi / (2 ** (j - i))
            qml.CRZ(angle, wires=[i, j])
    return qml.state()

allowed_ops = {"RX", "RY", "IsingXX"}

qnode = qml.QNode(circuit, dev)

compiled_qft = qml.compile(circuit, basis_set=allowed_ops)

compiled_qnode = qml.QNode(compiled_qft, dev)

print(qml.draw(compiled_qnode)())

# Print the circuit as ASCII art
# print(qml.draw(circuit)())
