from trap import create_trap_graph
from verifier import verifier

from numpy import pi

graph = create_trap_graph()


positions_history = [
        [(0,0),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3)],
        [(0,1),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3)],
        [(0,2),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3)],
        [(0,3),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3)]
]

gates_schedule = [
    [("RX", pi, 0)],
    [("RY", pi/2, 0)],
    [],
    []
]

# verifier(positions_history, gates_schedule, graph)

import pennylane as qml
mixed_device = qml.device("default.mixed", wires=8)
qml.Hadamard(wires=0)
qml.expval(qml.PauliZ(0))
