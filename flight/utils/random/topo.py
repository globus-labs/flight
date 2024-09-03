import networkx as nx

from flight.topo import Topology
from flight.topo.topology import REQUIRED_ATTRS


def random_topo(num_nodes: int, seed: int | None = None) -> Topology:
    """Generates a random Topology.

    Args:
        num_nodes (int): ...
        seed (int | None): ...

    Returns:
        A random Topology using ``networkx.random_tree()``.
    """
    tree = nx.random_tree(n=num_nodes, seed=seed, create_using=nx.DiGraph)
    for node in tree.nodes():
        for attr in REQUIRED_ATTRS:
            tree.nodes[node][attr] = None
    return Topology(tree)
