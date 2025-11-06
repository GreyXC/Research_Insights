import matplotlib.pyplot as plt
import networkx as nx

def visualize_author_graph(G, seed=1472, k=5, iterations=1000):
    pos = nx.spring_layout(G, seed=seed, k=k, iterations=iterations)

    weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(weights) if weights else 1
    edge_widths = [0.5 + 4 * (w / max_weight) for w in weights]
    edge_colors = [G.nodes[u]['cluster'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, alpha=0.4, connectionstyle='arc3,rad=0.2', arrows=True)

    node_sizes = [300 + 100 * G.degree(n) for n in G.nodes()]
    node_colors = [G.nodes[n]['cluster'] for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.tab10)

    for node, (x, y) in pos.items():
        font_size = 6 + 2 * (G.degree(node) / max(dict(G.degree()).values()))
        plt.text(x, y, node, fontsize=font_size, ha='center', va='center')

    plt.axis('off')
    plt.title("Author & Co-Authorship Network", fontsize=12)
    plt.tight_layout()
    plt.show()