import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

def visualize_author_graph(G, seed=1472, k=5, iterations=500):
    pos = nx.spring_layout(G, seed=seed, k=k, iterations=iterations)

    # Use semantic cluster if available
    cluster_attr = 'semantic_cluster' if 'semantic_cluster' in next(iter(G.nodes(data=True)))[1] else 'cluster'

    # Define fixed hex colors (tab10)
    hex_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                  '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                  '#bcbd22', '#17becf']

    # Map themes to hex colors
    themes = sorted(set(nx.get_node_attributes(G, cluster_attr).values()))
    theme_to_color = {
        theme: hex_colors[i % len(hex_colors)]
        for i, theme in enumerate(themes)
    }

    # Edge styling
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(weights) if weights else 1
    edge_widths = [0.5 + 4 * (w / max_weight) for w in weights]
    edge_colors = [theme_to_color.get(G.nodes[u].get(cluster_attr, ''), '#7f7f7f') for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, alpha=0.4)

    # Node styling
    node_sizes = [300 + 100 * G.degree(n) for n in G.nodes()]
    node_colors = [theme_to_color.get(G.nodes[n].get(cluster_attr, ''), '#7f7f7f') for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors)

    # Node labels
    for node, (x, y) in pos.items():
        theme = G.nodes[node].get(cluster_attr, 'N/A')
        label = f"{node}\n[{theme}]"
        font_size = 6 + 2 * (G.degree(node) / max(dict(G.degree()).values()))
        plt.text(x, y, label, fontsize=font_size, ha='center', va='center')

    # Legend
    handles = [
        mpatches.Patch(color=color, label=theme)
        for theme, color in theme_to_color.items()
    ]
    plt.legend(handles=handles, title="Author Fields", loc="lower left", fontsize=8, title_fontsize=9, frameon=True)

    plt.axis('on') 
    plt.title("Author Co-Authorship Network (Semantic Clusters)", fontsize=14)
    plt.tight_layout()
    plt.show()