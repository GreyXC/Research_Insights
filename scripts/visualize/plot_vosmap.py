import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

def plot_vos_map(clusters, cluster_names=None):
    # Create graph
    G = nx.Graph()

    # Track unique cluster labels and assign consistent colors
    unique_labels = sorted(set(cluster_names.values())) if cluster_names else sorted(clusters.keys())
    palette = sns.color_palette("hls", len(unique_labels))
    label_color_map = dict(zip(unique_labels, palette))

    # Track which keywords have already been added
    seen_terms = {}

    # Add nodes and edges
    for cluster_id, keywords in clusters.items():
        label = cluster_names.get(cluster_id, cluster_id) if cluster_names else cluster_id
        color = label_color_map[label]

        terms = [kw for kw, _ in keywords]

        for i, term in enumerate(terms):
            # Add node only once
            if term not in seen_terms:
                G.add_node(term, cluster=label, color=color)
                seen_terms[term] = label

        # Add edges between terms in the same cluster
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                G.add_edge(terms[i], terms[j])

    # Layout
    pos = nx.spring_layout(G, seed=42)

    # Draw nodes by cluster label
    plt.figure(figsize=(12, 8))
    for label in unique_labels:
        nodes = [n for n in G.nodes if G.nodes[n]['cluster'] == label]
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=[label_color_map[label]] * len(nodes), label=label)

    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_labels(G, pos, font_size=9)

    # Legend
    handles = [
        plt.Line2D([0], [0], marker='o', color='w', label=label,
                   markerfacecolor=label_color_map[label], markersize=10)
        for label in unique_labels
    ]
    plt.legend(handles=handles, title="Cluster", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.title("VOS-style Keyword Map")
    plt.axis("off")
    plt.tight_layout()
    plt.show()