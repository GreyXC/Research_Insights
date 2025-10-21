import plotly.graph_objects as go
from collections import defaultdict
import numpy as np
import math

def curved_edge(x0, y0, x1, y1, curvature=0.15):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    norm = np.sqrt(dx**2 + dy**2)
    if norm == 0:
        return [x0, x1, None], [y0, y1, None]
    ox, oy = -dy / norm, dx / norm
    cx, cy = mx + curvature * ox, my + curvature * oy
    return [x0, cx, x1, None], [y0, cy, y1, None]

def plot_interactive(G, term_freq, pos, sizing_mode="frequency", cluster_colors=None):
    cluster_nodes = defaultdict(list)
    cluster_edges = defaultdict(list)

    for node in G.nodes():
        cluster = G.nodes[node].get("cluster", "Unknown")
        cluster_nodes[cluster].append(node)

    for edge in G.edges():
        source, target = edge
        cluster = G.nodes[source].get("cluster", "Unknown")
        cluster_edges[cluster].append((source, target))

    traces = []

    for cluster, nodes in cluster_nodes.items():
        color = cluster_colors.get(cluster, "#CCCCCC") if cluster_colors else "#CCCCCC"
        node_x, node_y, node_text, node_size = [], [], [], []

        for node in nodes:
            x, y = pos[node]
            freq = term_freq.get(node, 1)
            degree = G.nodes[node].get("degree", 0)
            betweenness = G.nodes[node].get("betweenness", 0)

            if sizing_mode == "centrality":
                size = max(min(degree * 100, 60), 5)
            elif sizing_mode == "betweenness":
                size = max(min(betweenness * 1000, 60), 5)
            else:
                size = max(min(math.log(freq + 1) * 10, 60), 5)

            node_x.append(x)
            node_y.append(y)
            node_size.append(size)
            node_text.append(f"{node} ({freq})")

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

        edge_x, edge_y = [], []
        weights = []

        for source, target in cluster_edges[cluster]:
            x0, y0 = pos[source]
            x1, y1 = pos[target]
            cx, cy = curved_edge(x0, y0, x1, y1, curvature=0.15)
            edge_x += cx
            edge_y += cy
            weights.append(G[source][target].get("weight_norm", 0.5))

        avg_weight = sum(weights) / len(weights) if weights else 0.5
        edge_thickness = max(avg_weight * 4, 1)
        edge_opacity = min(avg_weight + 0.2, 1)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=edge_thickness, color='rgba(100,100,100,1)'),
            opacity=edge_opacity,
            hoverinfo='none',
            mode='lines',
            name=f"{cluster} edges",
            legendgroup=cluster,
            showlegend=False,
            visible=True
        )
        traces.append(edge_trace)

    sorted_traces = [t for t in traces if t.mode == 'lines'] + [t for t in traces if t.mode != 'lines']

    fig = go.Figure(
        data=sorted_traces,
        layout=go.Layout(
            title=dict(text='Neo4j-style Keyword Map', font=dict(size=16)),
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)
        )
    )

    fig.show()