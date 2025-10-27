import re
import subprocess
from collections import Counter

# Refresh PRISMA tracking: clean data, count stages, generate CSV
subprocess.run(["python", "-m", "scripts.clean.clean_data"], check=True)
subprocess.run(["python", "-m", "scripts.analysis.count_prisma_stages"], check=True)
subprocess.run(["python", "-m", "scripts.analysis.generate_prisma_csv"], check=True)

# Load modules
from scripts.load.load_json import load_mendeley_json
from scripts.analysis.cluster_keywords import cluster_keywords
from scripts.analysis.name_clusters import name_clusters
from scripts.visualize.plot_keywords import plot_keyword_bar_chart
from scripts.visualize.vosmapper.build_graph import build_graph
from scripts.visualize.vosmapper.compute_layout import compute_layout
from scripts.visualize.vosmapper.plot_interactive import plot_interactive

# Load cleaned metadata
df = load_mendeley_json("data_sources/raw/cleaned_metadata.json")

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

# Define the same palette used in name_clusters()
cluster_palette = {
    "Governance & Equity": "#FF7F0E",
    "Infrastructure Risk & Resilience": "#1F77B4",
    "Sustainable Systems & Access": "#2CA02C",
    "Urban Planning & Open Data": "#9467BD",
    "Crisis Modeling & Communication": "#D62728",
    "Urban Logistics & Mobility": "#8C564B",
    "Computational Modeling & Systems": "#E377C2",
    "Regional Environmental Hazards": "#7F7F7F",
    "Fallback": "#CCCCCC"
}

# Set number of clusters dynamically (excluding fallback)
n_clusters = len([k for k in cluster_palette if k != "Fallback"])

# Cluster keywords
clusters, filtered_lists = cluster_keywords(df, column="word_list", n_clusters=n_clusters, return_tokens=True)

# Assign semantic labels and color codes
cluster_names, cluster_colors = name_clusters(clusters)

# Build global term frequency from filtered tokens
flat_keywords = [kw for tokens in filtered_lists for kw in tokens]
term_freq = Counter(flat_keywords)

# Optional bar chart
plot_keyword_bar_chart(clusters, cluster_names)

# Build graph
G = build_graph(clusters, cluster_names)

# Filter nodes (frequency threshold + fallback inclusion)
visible_nodes = {n for n in G.nodes() if term_freq.get(n, 0) >= 5}

# Ensure at least one node per cluster is retained
for cluster_id, keywords in clusters.items():
    fallback_nodes = [node for node, _ in keywords if node in G.nodes() and node not in visible_nodes]
    if fallback_nodes:
        visible_nodes.add(fallback_nodes[0])

# Ensure every visible node has a frequency entry
for node in visible_nodes:
    term_freq.setdefault(node, 1)

# Rebuild graph and term_freq
G = G.subgraph(visible_nodes).copy()
term_freq = {k: v for k, v in term_freq.items() if k in visible_nodes}

# Tag isolated nodes (no edges)
for node in G.nodes():
    if G.degree(node) == 0:
        G.nodes[node]["isolated"] = True

# Identify isolated nodes (no edges)
isolated_nodes = [n for n in G.nodes() if G.degree(n) == 0]

# Optional: assign a fallback edge weight or tag for styling
for node in isolated_nodes:
    G.nodes[node]["isolated"] = True

# Compute layout
pos = compute_layout(G, layout_type="kamada")  # "kamada", "spring", "spectral", "circular"

# Render interactive map
plot_interactive(
    G,
    term_freq,
    pos,
    sizing_mode="co-occurrence",  # 'frequency' or 'co-occurrence'
    cluster_colors=cluster_colors,
    strong_edge_scale=0.5,
    weak_edge_scale=0.5,
    edge_threshold=0.1
)