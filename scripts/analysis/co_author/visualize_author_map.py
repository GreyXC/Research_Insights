import matplotlib.pyplot as plt
import networkx as nx

def visualize_author_graph(G, seed=1472, k=5, iterations=500):
    pos = nx.spring_layout(G, seed=seed, k=k, iterations=iterations)

    # Use semantic cluster if available
    cluster_attr = 'semantic_cluster' if 'semantic_cluster' in next(iter(G.nodes(data=True)))[1] else 'cluster'

    weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(weights) if weights else 1
    edge_widths = [0.5 + 4 * (w / max_weight) for w in weights]
    edge_colors = [G.nodes[u].get(cluster_attr, 0) for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, alpha=0.4)

    node_sizes = [300 + 100 * G.degree(n) for n in G.nodes()]
    node_colors = [G.nodes[n].get(cluster_attr, 0) for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.tab10)

    for node, (x, y) in pos.items():
        font_size = 6 + 2 * (G.degree(node) / max(dict(G.degree()).values()))
        plt.text(x, y, node, fontsize=font_size, ha='center', va='center')

    plt.axis('off')
    plt.title("Author Co-Authorship Network (Semantic Clusters)", fontsize=14)
    plt.tight_layout()
    plt.show()