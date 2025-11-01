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
    weak_edge_scale=1.0,
    edge_threshold=0.05
):
    cluster_nodes = defaultdict(list)
    cluster_edges = defaultdict(list)

    # ✅ Group by semantic label instead of raw cluster ID
    for node in G.nodes():
        label = G.nodes[node].get("label", G.nodes[node].get("cluster", "Unknown"))
        cluster_nodes[label].append(node)

    for source, target in G.edges():
        label = G.nodes[source].get("label", G.nodes[source].get("cluster", "Unknown"))
        cluster_edges[label].append((source, target))

    traces = []
    visible_nodes = set(pos.keys())

    for label, nodes in cluster_nodes.items():
        color = cluster_colors.get(label, "#CCCCCC") if cluster_colors else "#CCCCCC"
        regular_x, regular_y, regular_text, regular_size = [], [], [], []
        isolated_x, isolated_y, isolated_text, isolated_size = [], [], [], []

        for node in nodes:
            if node not in pos:
                continue
            x, y = pos[node]
            is_isolated = G.degree(node) == 0

            if sizing_mode == "frequency":
                freq = term_freq.get(node, 1)
                size = max(min((freq + 1) ** 1.2 * 1, 500), 0.5)
                label_text = f"{node} ({freq})"
            elif sizing_mode == "co-occurrence":
                weight_sum = sum(G[node][nbr].get("weight", 1) for nbr in G.neighbors(node))
                size = max(min((weight_sum + 1) ** 1.1 * 1, 500), 0.5)
                label_text = f"{node} ({int(weight_sum)})"
            else:
                size = 0.5
                label_text = node

            if is_isolated:
                isolated_x.append(x)
                isolated_y.append(y)
                isolated_text.append(label_text)
                isolated_size.append(size)
            else:
                regular_x.append(x)
                regular_y.append(y)
                regular_text.append(label_text)
                regular_size.append(size)

        # Regular node trace
        traces.append(go.Scatter(
            x=regular_x, y=regular_y,
            mode='markers+text',
            text=regular_text,
            textposition='top center',
            hoverinfo='text',
            marker=dict(
                size=regular_size,
                color=color,
                line=dict(width=0.5, color='black')
            ),
            name=label,
            legendgroup=label,
            showlegend=True,
            visible=True
        ))

        # Isolated node trace
        traces.append(go.Scatter(
            x=isolated_x, y=isolated_y,
            mode='markers+text',
            text=isolated_text,
            textposition='top center',
            hoverinfo='text',
            marker=dict(
                size=isolated_size,
                color=color,
                line=dict(width=10, color="#B91818")
            ),
            name=f"{label} (isolated)",
            legendgroup=label,
            showlegend=False,
            visible=True
        ))

        for source, target in cluster_edges[label]:
            if source not in visible_nodes or target not in visible_nodes:
                continue
            x0, y0 = pos[source]
            x1, y1 = pos[target]
            distance = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
            resolution = int(min(max(distance * 0.5, 10), 30))
            cx, cy = curved_edge(x0, y0, x1, y1, curvature=0.15, resolution=resolution)
            weight = G[source][target].get("weight_norm", 0.5)
            thickness = compute_thickness(weight, strong_edge_scale, weak_edge_scale)
            opacity = compute_opacity(weight, strong_edge_scale, weak_scale=weak_edge_scale)
            color_rgba = f"rgba(100, 100, 100, {opacity:.3f})"

            edge_trace = go.Scatter(
                x=cx, y=cy,
                line=dict(width=thickness, color=color_rgba),
                hoverinfo='none',
                mode='lines',
                name=f"{label} edge",
                legendgroup=label,
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