import networkx as nx
from collections import defaultdict

def build_graph(clusters, cluster_names):
    """
    Builds a co-occurrence graph from clustered keywords.
    Tags nodes with cluster ID and semantic label.
    """
    G = nx.Graph()
    keyword_to_cluster = {}

    # Add nodes with cluster and label
    for cluster_id, keywords in clusters.items():
        label = cluster_names.get(cluster_id, "Unknown")
        for keyword, _ in keywords:
            keyword_to_cluster.setdefault(keyword, set()).add(cluster_id)
            G.add_node(keyword, cluster=cluster_id, label=label)

    # Build co-occurrence edges
    cooccurrence = defaultdict(int)
    for cluster_id, keywords in clusters.items():
        tokens = [kw for kw, _ in keywords]
        for i in range(len(tokens)):
            for j in range(i + 1, len(tokens)):
                pair = tuple(sorted((tokens[i], tokens[j])))
                cooccurrence[pair] += 1

    for (kw1, kw2), weight in cooccurrence.items():
        G.add_edge(kw1, kw2, weight=weight)

    # Optional: tag bridge nodes
    for node in G.nodes():
        neighbor_clusters = {G.nodes[n].get("cluster") for n in G.neighbors(node)}
        if len(neighbor_clusters) > 1:
            G.nodes[node]["bridge"] = True

    return G