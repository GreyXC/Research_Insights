import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx
import seaborn as sns
import numpy as np
import alphashape
from shapely.geometry import Polygon

def draw_cluster_shape(ax, pos, nodes, color, alpha=0.2):
    points = np.array([pos[n] for n in nodes])
    if len(points) < 4:
        return
    shape = alphashape.alphashape(points, alpha=0.3)
    if isinstance(shape, Polygon):
        x, y = shape.exterior.xy
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=color)

def bucket_size(freq, scale=0.8):
    if freq < 3:
        return int(50 * scale)   # Least frequent
    elif freq < 15:
        return int(200 * scale)  # Medium range
    else:
        return int(900 * scale)  # Most frequent

def font_size_from_node_size(size):
    return max(6, min(7, int(size / 60)))  # Scales font size between 6 and 7

def plot_vos_map(clusters, cluster_names=None, scale=1.0):
    G = nx.Graph()

    # Assign consistent colors to unique cluster labels
    unique_labels = sorted(set(cluster_names.values())) if cluster_names else sorted(clusters.keys())
    palette = sns.color_palette("hls", len(unique_labels))
    label_color_map = dict(zip(unique_labels, palette))

    seen_terms = {}
    term_freq = {}

    # Add nodes and weighted edges
    for cluster_id, keywords in clusters.items():
        label = cluster_names.get(cluster_id, cluster_id) if cluster_names else cluster_id
        color = label_color_map[label]
        terms = [kw for kw, _ in keywords]

        for kw, count in keywords:
            term_freq[kw] = count
            if kw not in seen_terms:
                G.add_node(kw, cluster=label, color=color)
                seen_terms[kw] = label

        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                if G.has_edge(terms[i], terms[j]):
                    G[terms[i]][terms[j]]['weight'] += 1
                else:
                    G.add_edge(terms[i], terms[j], weight=1)

    # Improved spacing with spring layout
    pos = nx.spring_layout(G, seed=1472, k=5, iterations=500)

    fig, ax = plt.subplots(figsize=(12, 8))

    # Build node size map
    node_size_map = {n: bucket_size(term_freq.get(n, 1), scale=scale) for n in G.nodes}

    # Draw organic cluster shapes and nodes
    for label in unique_labels:
        nodes = [n for n in G.nodes if G.nodes[n]['cluster'] == label]
        color = label_color_map[label]
        draw_cluster_shape(ax, pos, nodes, color)

        sizes = [node_size_map[n] for n in nodes]
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=[color] * len(nodes), node_size=sizes, label=label)

    # Normalize edge weights and style by cluster relation
    # materialize the edge view to a list so type-checkers accept it
    edgelist = list(G.edges(data=True))
    max_weight = max(edge[2]['weight'] for edge in edgelist) if edgelist else 1
    widths = [edge[2]['weight'] / max_weight * 2.5 for edge in edgelist]
    edge_colors = [
        'black' if G.nodes[u]['cluster'] == G.nodes[v]['cluster'] else 'gray'
        for u, v, _ in edgelist
    ]

    # Draw curved edges with color and weight
    nx.draw_networkx_edges(
        G, pos,
        edgelist=edgelist,
        width=widths,
        edge_color=edge_colors,
        alpha=0.4,
        connectionstyle='arc3,rad=0.1'
    )

    # Draw labels with font size scaled by node size
    for node, (x, y) in pos.items():
        label = node
        size = node_size_map.get(node, 100)
        font_size = font_size_from_node_size(size)
        ax.text(
            x, y, label,
            fontsize=font_size,
            fontweight='bold',
            color='black',
            ha='center', va='center'
            # Uncomment below to enable label background
            # bbox=dict(
            #     facecolor=(0.2, 0.2, 0.2, 0.1),
            #     edgecolor='black',
            #     boxstyle='round,pad=0.3'
            # )
        )

    # Legend
    handles = [
        Line2D([0], [0], marker='o', color='w', label=label,
               markerfacecolor=label_color_map[label], markersize=10)
        for label in unique_labels
    ]
    ax.legend(handles=handles, title="Cluster", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.title("VOS-style Keyword Map (Enhanced Connectivity & Scaled Labels)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()