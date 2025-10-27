import networkx as nx

def compute_layout(G, layout_type="spring", seed=1472, k=5, iterations=1000):
    layout_type = layout_type.lower()

    """
    Computes node positions for a graph G using the specified layout algorithm.

    Parameters:
    - G: NetworkX graph
    - layout_type: "spring", "kamada", "spectral", or "circular"
    - seed: random seed for reproducibility (used in spring layout)
    - k: optimal distance between nodes (spring layout only)
    - iterations: number of iterations (spring layout only)

    Returns:
    - pos: dictionary of node positions
    """


    if layout_type == "spring":
        return nx.spring_layout(G, seed=seed, k=k, iterations=iterations)
    elif layout_type in ["kamada", "kamada_kawai"]:
        return nx.kamada_kawai_layout(G)
    elif layout_type == "spectral":
        return nx.spectral_layout(G)
    elif layout_type == "circular":
        return nx.circular_layout(G)
    else:
        raise ValueError(f"Unsupported layout type: {layout_type}")