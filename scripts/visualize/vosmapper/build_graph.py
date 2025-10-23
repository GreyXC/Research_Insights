import networkx as nx

def clean_kw(kw):
    return kw[0].strip().lower() if isinstance(kw, tuple) else kw.strip().lower()

def build_graph(clusters, cluster_names):
    G = nx.Graph()

    for cluster_id, keywords in clusters.items():
        label = cluster_names.get(cluster_id, f"Cluster {cluster_id}")
        for kw in keywords:
            kw_clean = clean_kw(kw)
            G.add_node(kw_clean, cluster=label)

    for keywords in clusters.values():
        clean_keywords = [clean_kw(kw) for kw in keywords]
        for i, kw1 in enumerate(clean_keywords):
            for kw2 in clean_keywords[i+1:]:
                if G.has_edge(kw1, kw2):
                    G[kw1][kw2]['weight'] += 1
                else:
                    G.add_edge(kw1, kw2, weight=1)

    max_weight = max(d['weight'] for _, _, d in G.edges(data=True))
    for u, v, d in G.edges(data=True):
        d['weight_norm'] = d['weight'] / max_weight

    return G