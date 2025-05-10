import numpy as np

def cnot(ctrl, trg, positions):
    gates = []
    gates.append([("RY", np.pi / 2, positions[ctrl])])
    gates.append([("MS", np.pi / 4, (positions[ctrl], positions[trg]))])
    gates.append([("RX", np.pi / 2, positions[trg]), ("RX", np.pi / 2, positions[ctrl])])
    gates.append([("RY", -np.pi / 2, positions[ctrl])])
    return gates

