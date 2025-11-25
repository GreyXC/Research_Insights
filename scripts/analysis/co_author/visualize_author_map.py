import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
from random import uniform
from scipy.spatial import ConvexHull
from scipy.interpolate import splprep, splev
import matplotlib.patheffects as pe

def apply_jitter(pos, scale=0.01):
    return {
        node: (x + uniform(-scale, scale), y + uniform(-scale, scale))
        for node, (x, y) in pos.items()
    }

def draw_cluster_hull_smooth(ax, pos, nodes, color="#1f77b4", alpha=0.1, padding=0.2, smoothness=50):
    points = np.array([pos[n] for n in nodes if n in pos])
    if len(points) < 3:
        print(f"Skipping hull: only {len(points)} points")
        return

    hull = ConvexHull(points)
    polygon = points[hull.vertices]

    # Expand outward from centroid
    centroid = np.mean(polygon, axis=0)
    expanded = centroid + (polygon - centroid) * (1 + padding)
    expanded = np.vstack([expanded, expanded[0]])  # Close polygon

    # Interpolate smooth curve
    x, y = expanded[:, 0], expanded[:, 1]
    tck, _ = splprep([x, y], s=0, per=True)
    xi, yi = splev(np.linspace(0, 1, smoothness), tck)

    ax.fill(xi, yi, color=color, alpha=alpha, zorder=0)

def visualize_author_graph(G, seed=1472, k=0.5, iterations=10, cluster_expand=0.5):
    # Prepare a layout-specific edge weight that reduces attraction for very
    # heavily-weighted edges. By inverting the original weight we make strong
    # co-authorship links pull less during spring layout, which helps reduce
    # crowding in dense regions.
    for u, v, data in G.edges(data=True):
        try:
            w = float(data.get('weight', 1.0))
        except Exception:
            w = 1.0
        data['layout_weight'] = 1.0 / (1.0 + w)

    if all('layout_seed' in G.nodes[n] for n in G.nodes()):
        seed_pos = {n: G.nodes[n]['layout_seed'] for n in G.nodes()}
        pos = nx.spring_layout(G, pos=seed_pos, seed=seed, k=k, iterations=iterations, weight='layout_weight')
        pos = apply_jitter(pos, scale=0.1)
    else:
        pos = nx.spring_layout(G, seed=seed, k=k, iterations=iterations, weight='layout_weight')

    cluster_attr = 'semantic_cluster' if 'semantic_cluster' in next(iter(G.nodes(data=True)))[1] else 'cluster'

    # Normalize layout positions to simple float tuples to avoid array typing issues
    pos = {n: (float(p[0]), float(p[1])) for n, p in pos.items()}

    # Optional: expand nodes within each cluster away from the cluster centroid
    # to reduce intra-cluster overlap for dense clusters. `cluster_expand` is a
    # multiplier controlling how strongly nodes are pushed outward (0=no change).
    if cluster_expand and cluster_expand > 0:
        # Group nodes by cluster
        clusters = {}
        for n in G.nodes():
            attr = G.nodes[n].get(cluster_attr, None)
            clusters.setdefault(attr, []).append(n)

        # Find maximum cluster size for normalization
        max_size = max((len(v) for v in clusters.values()), default=1)

        # For each cluster, push nodes away from centroid proportionally to size
        for attr, nodes in clusters.items():
            if not nodes:
                continue
            pts = [pos[n] for n in nodes if n in pos]
            if not pts:
                continue
            centroid = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
            size = len(nodes)
            # Normalized factor in [0,1], larger clusters push more
            norm = float(size) / float(max_size)
            factor = 1.0 + cluster_expand * norm
            for n in nodes:
                if n not in pos:
                    continue
                x, y = pos[n]
                vx = x - centroid[0]
                vy = y - centroid[1]
                # If node is at centroid, jitter it first
                if abs(vx) < 1e-6 and abs(vy) < 1e-6:
                    vx, vy = (uniform(-0.01, 0.01), uniform(-0.01, 0.01))
                pos[n] = (centroid[0] + vx * factor, centroid[1] + vy * factor)

    cluster_attr = 'semantic_cluster' if 'semantic_cluster' in next(iter(G.nodes(data=True)))[1] else 'cluster'

    hex_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                  '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                  '#bcbd22', '#17becf']
    themes = sorted(set(nx.get_node_attributes(G, cluster_attr).values()))
    theme_to_color = {theme: hex_colors[i % len(hex_colors)] for i, theme in enumerate(themes)}

    print("Available cluster labels:", themes)

    fig, ax = plt.subplots(figsize=(15, 10))

    # Draw smooth padded hulls for all clusters
    for theme in themes:
        cluster_nodes = [n for n in G.nodes if G.nodes[n].get(cluster_attr) == theme]
        print(f"Hull: {theme}, node count: {len(cluster_nodes)}")
        #draw_cluster_hull_smooth(ax, pos, cluster_nodes, color=theme_to_color[theme], alpha=0.1, padding=0.2) # uncomment to enable hull

    # Draw edges
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(weights) if weights else 1
    edge_widths = [0.5 + 4 * (w / max_weight) for w in weights]
    edge_colors = [theme_to_color.get(G.nodes[u].get(cluster_attr, ''), '#7f7f7f') for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, alpha=0.4, ax=ax)

    # Draw nodes
    node_sizes = [200 + 100 * G.degree(n) for n in G.nodes()]
    node_colors = [theme_to_color.get(G.nodes[n].get(cluster_attr, ''), '#7f7f7f') for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, ax=ax)

    # Draw labels
    max_degree = max(dict(G.degree()).values()) if G.number_of_nodes() > 0 else 1
    for node, (x, y) in pos.items():
        theme = G.nodes[node].get(cluster_attr, 'N/A')
        label = f"{node}"
        font_size = 6 + 1 * (G.degree(node) / max_degree)

        txt = ax.text(
            x, y, label,
            fontsize=font_size,
            ha='center', va='center',
            color='black',
            zorder=3
        )
        # Add a white stroke behind the text for contrast against any background
        txt.set_path_effects([
            pe.withStroke(linewidth=2, foreground='white'),
            pe.Normal()
        ])

    # Legend
    handles = [mpatches.Patch(color=color, label=theme) for theme, color in theme_to_color.items()]
    ax.legend(handles=handles, title="Author Fields", loc="lower left", fontsize=8, title_fontsize=9, frameon=True)

    ax.axis('on') # Turn on/off axis
    ax.set_title("Co-Authorship Network (With Topic Modelled Semantic Groups)", fontsize=14)
    plt.tight_layout()
    plt.show()