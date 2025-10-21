import networkx as nx

def compute_layout(G, layout="kamada_kawai", seed=1472, k=5, iterations=500):
    if layout == "spring":
        return nx.spring_layout(G, seed=seed, k=k, iterations=iterations)
    elif layout == "kamada_kawai":
        return nx.kamada_kawai_layout(G)
    elif layout == "spectral":
        return nx.spectral_layout(G)
    else:
        raise ValueError(f"Unsupported layout type: {layout}")