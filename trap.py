import networkx as nx
from mpl_toolkits.mplot3d import Axes3D


def create_trap_graph():
    """Create a graph representing the Penning trap."""

    trap = nx.Graph()

    rows = 5
    cols = 7

    interaction_nodes = [(1, 1), (1, 3), (3, 1), (3, 3), (1, 5), (3, 5)]

    for r in range(rows):
        for c in range(cols):
            base_node_id = (r, c)

            if base_node_id in interaction_nodes:
                trap.add_node(base_node_id, type="interaction")
            else:
                trap.add_node(base_node_id, type="standard")
                rest_node_id = (r, c, "idle")
                trap.add_node(rest_node_id, type="idle")
                trap.add_edge(base_node_id, rest_node_id)

    for r in range(rows):
        for c in range(cols):
            node_id = (r, c)
            if c + 1 < cols:
                neighbor_id = (r, c + 1)
                trap.add_edge(node_id, neighbor_id)
            if r + 1 < rows:
                neighbor_id = (r + 1, c)
                trap.add_edge(node_id, neighbor_id)
    return trap
