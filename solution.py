import numpy as np
from transpile_qiskit import layers
from trap import create_trap_graph
from verifier import verifier

initial_positions = [(0,0), (0,1), (0,2), (1,2), (2,2), (2,1), (2,0), (1,0)]
positions = [0, 1, 2, 3, 4, 5, 6, 7]



# Does a circular permutation around the interaction node.
def circular_permutation():
    for i in range(8):
        if positions[i] != -1:
            positions[i] = (positions[i] + 1) % 8
    # need to add a gate time step!!!!!!!!!!



# We want to do an MS gate on q1 and q2, but neither of them is in the center.
# Thus, we move them to the center.
def move_2_to_center(q1, q2):
    # Check if there are any qubits in the center and try to move them out.
    free_positions = [pos for pos in range(8) if pos not in positions]
    for q in range(8):
        if positions[q] == -1 and len(free_positions) > 0:
            positions[q] = free_positions.pop()

    # Permute if needed.
    if (positions[q1] - positions[q2]) % 2 == 1 or positions[q1] % 2 == 0 or positions.count(-1) > 0:
        circular_permutation()

    free_positions = [pos for pos in range(8) if pos not in positions]
    for q in range(8):
        if positions[q] == -1 and len(free_positions) > 0:
            positions[q] = free_positions.pop()

    positions[q1] = -1
    positions[q2] = -1



# We want to do an MS gate on q1 and q2, but only q2 is in the center.
# Thus, we move q1 to the center.
def move_1_to_center(q1, q2):
    # Check if there is another qubit besides q2 in the center and move it out.
    free_positions = [pos for pos in range(8) if pos not in positions]
    for q in range(8):
        if q == q2:
            continue
        if positions[q] == -1 and len(free_positions) > 0:
            positions[q] = free_positions.pop()

    # Permute if we cannot bring q1 directly to the center or if we still need to take a qubit out of the center.
    if positions[q1] % 2 == 0 or positions.count(-1) > 1:
        circular_permutation()

    # Try again to take qubit out.
    free_positions = [pos for pos in range(8) if pos not in positions]
    for q in range(8):
        if q == q2:
            continue
        if positions[q] == -1 and len(free_positions) > 0:
            positions[q] = free_positions.pop()

    # Move our qubit to the center.
    positions[q1] = -1



# If we want to move qubits out of the center (if they are in the center) to perform single-qubit gates on them.
def move_out(qubits):
    free_positions = [pos for pos in range(8) if pos not in positions]

    # Check if we still need to do the permutation in order to take the qubits out of the center.
    should_permute = False
    for q in qubits:
        # Take qubit out if we can.
        if positions[q] == -1 and len(free_positions) > 0:
            positions[q] = free_positions.pop()
        # Remember that we couldn't take a qubit out and that we need to permute.
        elif positions[q] == -1 and len(free_positions) <= 0:
            should_permute = True
    # Permute and try again.
    if should_permute == True:
        circular_permutation()
        free_positions = [pos for pos in range(8) if pos not in positions]
        for q in qubits:
            if positions[q] == -1 and len(free_positions) > 0:
                positions[q] = free_positions.pop()




positions_history = []

for layer in layers:
    positions_history.append(list(positions))
    count_ms = [gate[0] for gate in layer].count("MS")

    if count_ms == 0:
        # Find the qubits that need to be out of the center.
        gate_qubits = set()
        for gate in layer:
            gate_qubits.add(gate[2])
        # If they are in the center, move them out.
        move_out(gate_qubits)

    elif count_ms == 1:
        for gate in layer:
            if gate[0] == "MS":
                ms = gate
        # Find the ions on which the gate acts.
        to_ms1 = ms[2][0]
        to_ms2 = ms[2][1]

        # Make sure both ions are in the center.
        if positions[to_ms1] != -1 and positions[to_ms2] != -1:
            move_2_to_center(to_ms1, to_ms2)
        elif positions[to_ms1] == -1 and positions[to_ms2] != -1:
            move_1_to_center(to_ms2, to_ms1)
        elif positions[to_ms1] != -1 and positions[to_ms2] == -1:
            move_1_to_center(to_ms1, to_ms2)
    else:
        print(layer)
        raise Exception("two rxx in the same layer")


print(verifier(positions_history, layers, create_trap_graph()))