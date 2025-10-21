import networkx as nx

def compute_layout(G, seed=1472, k=5, iterations=1000):
    pos = nx.spring_layout(G, seed=seed, k=k, iterations=iterations)
    return pos