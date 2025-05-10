import pennylane as qml
import numpy as np
import transpile_qiskit
import math

from transpile_qiskit import layers

gate_schedule = layers
mixed_device = qml.device("default.mixed", wires=8)


@qml.qnode(device=mixed_device)
def circuit():
    qml.QFT(wires=range(8))
    return qml.density_matrix(wires=range(8))


def compiled_circuit(gates_schedule) -> qml.QNode:
    """
    Build the compiled circuit from the gates schedule.

    Args:
        gates_schedule (list): A list of gates where each gate is represented as a tuple.

    Returns:
        qml.QNode: A Pennylane QNode representing the circuit.
    """

    @qml.qnode(device=mixed_device)
    def circuit():
        for step in gates_schedule:
            for gate in step:
                if gate[0] == "RX":
                    qml.RX(gate[1], wires=gate[2])
                elif gate[0] == "RY":
                    qml.RY(gate[1], wires=gate[2])
                elif gate[0] == "MS":
                    qml.IsingXX(gate[1], wires=gate[2])
        return qml.density_matrix(wires=range(8))

    return circuit


expected_result = circuit()
user_result = compiled_circuit(gate_schedule)()

# print(expected_result)
# print(user_result)

if not np.allclose(expected_result, user_result, atol=1e-5):
    raise ValueError("The 2 circuits are not the same.")
print("The compiled circuit implements QFT(8).")