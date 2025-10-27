import plotly.graph_objects as go
from collections import defaultdict
import numpy as np
import math

def curved_edge(x0, y0, x1, y1, curvature=0.05, resolution=50):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    norm = np.sqrt(dx**2 + dy**2)
    if norm == 0:
        return [x0, x1, None], [y0, y1, None]

    ox, oy = -dy / norm, dx / norm
    cx, cy = mx + curvature * ox, my + curvature * oy

    t_vals = np.linspace(0, 1, resolution)
    x_vals = (1 - t_vals)**2 * x0 + 2 * (1 - t_vals) * t_vals * cx + t_vals**2 * x1
    y_vals = (1 - t_vals)**2 * y0 + 2 * (1 - t_vals) * t_vals * cy + t_vals**2 * y1

    return list(x_vals) + [None], list(y_vals) + [None]

def compute_thickness(weight, strong_scale=1.0, weak_scale=1.0, base=0.5, power=2.5, range=10):
    scaled = base + (weight ** power) * range
    return max(scaled * (strong_scale if weight >= 0.3 else weak_scale), 0.5)

def compute_opacity(weight, strong_scale=1.0, weak_scale=1.0, base=0.1, power=2.5, range=2.0):
    scaled = base + (weight ** power) * range
    return min(scaled * (strong_scale if weight >= 0.3 else weak_scale), 1.0)

def plot_interactive(
    G,
    term_freq,
    pos,
    sizing_mode="co-occurrence",
    cluster_colors=None,
    strong_edge_scale=1.0,
    weak_edge_scale=1.0
):
    cluster_nodes = defaultdict(list)
    cluster_edges = defaultdict(list)

    for node in G.nodes():
        cluster = G.nodes[node].get("cluster", "Unknown")
        cluster_nodes[cluster].append(node)

    for source, target in G.edges():
        cluster = G.nodes[source].get("cluster", "Unknown")
        cluster_edges[cluster].append((source, target))

    traces = []
    visible_nodes = set(pos.keys())

    for cluster, nodes in cluster_nodes.items():
        color = cluster_colors.get(cluster, "#CCCCCC") if cluster_colors else "#CCCCCC"
        node_x, node_y, node_text, node_size = [], [], [], []

        for node in nodes:
            if node not in pos:
                continue
            x, y = pos[node]
            if sizing_mode == "frequency":
                freq = term_freq.get(node, 1)
                size = max(min(math.log(freq + 1) * 10, 60), 0.5)
                label = f"{node} ({freq})"
            elif sizing_mode == "co-occurrence":
                weight_sum = sum(G[node][nbr].get("weight", 1) for nbr in G.neighbors(node))
                size = max(min(math.log(weight_sum + 1) * 10, 60), 0.5)
                label = f"{node} ({int(weight_sum)})"
            else:
                size = 10
                label = node

            node_x.append(x)
            node_y.append(y)
            node_size.append(size)
            node_text.append(label)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition='top center',
            hoverinfo='text',
            marker=dict(
                size=node_size,
                color=color,
                line=dict(width=0.5, color='black')
            ),
            name=cluster,
            legendgroup=cluster,
            showlegend=True,
            visible=True
        )
        traces.append(node_trace)

        for source, target in cluster_edges[cluster]:
            if source not in visible_nodes or target not in visible_nodes:
                continue
            x0, y0 = pos[source]
            x1, y1 = pos[target]
            distance = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
            resolution = int(min(max(distance * 0.5, 10), 30))
            cx, cy = curved_edge(x0, y0, x1, y1, curvature=0.15, resolution=resolution)
            weight = G[source][target].get("weight_norm", 0.5)
            thickness = compute_thickness(weight, strong_edge_scale, weak_edge_scale)
            opacity = compute_opacity(weight, strong_edge_scale, weak_edge_scale)
            color = f"rgba(100, 100, 100, {opacity:.3f})"

            edge_trace = go.Scatter(
                x=cx, y=cy,
                line=dict(width=thickness, color=color),
                hoverinfo='none',
                mode='lines',
                name=f"{cluster} edge",
                legendgroup=cluster,
                showlegend=False,
                visible=True
            )
            traces.append(edge_trace)

    sorted_traces = [t for t in traces if t.mode == 'lines'] + [t for t in traces if t.mode != 'lines']

    fig = go.Figure(
        data=sorted_traces,
        layout=go.Layout(
            title=dict(text=sizing_mode, font=dict(size=16)),
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)
        )
    )

    fig.show()