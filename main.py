import re
from collections import Counter
from scripts.load.load_json import load_mendeley_json
from scripts.analysis.cluster_keywords import cluster_keywords
from scripts.analysis.name_clusters import name_clusters
from scripts.visualize.plot_keywords import plot_keyword_bar_chart
from scripts.visualize.vosmapper.build_graph import build_graph
from scripts.visualize.vosmapper.compute_layout import compute_layout
from scripts.visualize.vosmapper.plot_interactive import plot_interactive

# Load metadata
df = load_mendeley_json("data_sources/raw/mendeley_metadata.json")

# Dynamically select available metadata fields
available_fields = ["title", "abstract", "keywords", "subject_area"]
existing_fields = [col for col in available_fields if col in df.columns]

# Extract all individual words from metadata fields
def extract_words(row):
    words = []
    for col in existing_fields:
        val = row[col]
        if isinstance(val, list):
            words.extend([str(v).strip().lower() for v in val])
        elif isinstance(val, str):
            tokens = re.findall(r"\b[a-zA-Z]{3,}\b", val.lower())
            words.extend(tokens)
    return words

df["word_list"] = df.apply(extract_words, axis=1)

# Cluster keywords and get filtered token lists
clusters, filtered_lists = cluster_keywords(df, column="word_list", return_tokens=True)

# Assign semantic labels and color codes
cluster_names, cluster_colors = name_clusters(clusters)

# Build global term frequency from filtered tokens
flat_keywords = [kw for tokens in filtered_lists for kw in tokens]
term_freq = Counter(flat_keywords)

# Optional bar chart
plot_keyword_bar_chart(clusters, cluster_names)

# Build graph
G = build_graph(clusters, cluster_names)

# Filter nodes (optional threshold)
visible_nodes = {n for n in G.nodes() if term_freq.get(n, 0) >= 5}
G = G.subgraph(visible_nodes).copy()
term_freq = {k: v for k, v in term_freq.items() if k in visible_nodes}

# Compute layout
pos = compute_layout(G, layout_type="kamada")

# Render interactive map
plot_interactive(
    G,
    term_freq,
    pos,
    sizing_mode="frequency", #"frequency" or "co-occurrence"
    cluster_colors=cluster_colors,
    strong_edge_scale=0.5,
    weak_edge_scale=0.1
)