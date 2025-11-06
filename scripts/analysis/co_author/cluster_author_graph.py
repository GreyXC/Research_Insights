import networkx as nx
import community as louvain

def cluster_author_graph(matrix):
    G = nx.from_pandas_adjacency(matrix)
    partition = louvain.best_partition(G)
    nx.set_node_attributes(G, partition, 'cluster')
    return G