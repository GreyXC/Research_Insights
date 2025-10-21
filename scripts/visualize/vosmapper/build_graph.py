import networkx as nx
from collections import Counter

def build_graph(clusters, cluster_names):
    G = nx.Graph()
    term_freq = Counter()

    for cluster_id, keywords in clusters.items():
        label = cluster_names.get(cluster_id, f"Cluster {cluster_id}")
        for kw in keywords:
            kw = kw[0] if isinstance(kw, tuple) else kw
            term_freq[kw] += 1
            G.add_node(kw, cluster=label)

    for keywords in clusters.values():
        clean_keywords = [kw[0] if isinstance(kw, tuple) else kw for kw in keywords]
        for i, kw1 in enumerate(clean_keywords):
            for kw2 in clean_keywords[i+1:]:
                if G.has_edge(kw1, kw2):
                    G[kw1][kw2]['weight'] += 1
                else:
                    G.add_edge(kw1, kw2, weight=1)

    max_weight = max(d['weight'] for _, _, d in G.edges(data=True))
    for u, v, d in G.edges(data=True):
        d['weight_norm'] = d['weight'] / max_weight

    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    for node in G.nodes():
        G.nodes[node]['degree'] = degree.get(node, 0)
        G.nodes[node]['betweenness'] = betweenness.get(node, 0)

    return G, term_freq