from scripts.load.load_json import load_mendeley_json
from scripts.analysis.cluster_keywords import cluster_keywords
from scripts.analysis.name_clusters import name_clusters
from scripts.visualize.plot_keywords import plot_keyword_bar_chart
from scripts.visualize.vosmapper.build_graph import build_graph
from scripts.visualize.vosmapper.compute_layout import compute_layout
from scripts.visualize.vosmapper.plot_interactive import plot_interactive

# Load metadata
df = load_mendeley_json("data_sources/raw/mendeley_metadata.json")

# Cluster keywords from abstract
clusters = cluster_keywords(df, column="abstract")

# Assign semantic labels and color codes
cluster_names, cluster_colors = name_clusters(clusters)

# Bar chart (optional)
plot_keyword_bar_chart(clusters, cluster_names)

# Build graph and compute term frequency
G, term_freq = build_graph(clusters, cluster_names)

# Compute layout
pos = compute_layout(G, layout="kamada_kawai")

# Render interactive map
plot_interactive(
    G,
    term_freq,
    pos,
    sizing_mode="frequency",
    cluster_colors=cluster_colors
)