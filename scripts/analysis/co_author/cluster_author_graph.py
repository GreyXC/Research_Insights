import networkx as nx

def cluster_author_graph(matrix, semantic_labels=None):
    G = nx.from_pandas_adjacency(matrix)
    if semantic_labels:
        nx.set_node_attributes(G, semantic_labels, 'semantic_cluster')
    return G