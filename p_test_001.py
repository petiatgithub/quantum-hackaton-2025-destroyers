from trap import create_trap_graph
from verifier import verifier

from math import pi

graph = create_trap_graph()


positions_history = [
        [(0,0),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3)],
        [(0,1),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3)],
        [(0,2),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3)],
        [(0,3),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3)]
]

gates_schedule = [
    [("RX", pi, 0)],
    [],
    [],
    []
]

verifier(positions_history, gates_schedule, graph)

