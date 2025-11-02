import re
import subprocess
from pathlib import Path
from collections import Counter
import time

# Reset PRISMA logs BEFORE any subprocess runs
log_dir = Path("data_sources_raw/logs")
counts_path = log_dir / "prisma_counts.json"
decisions_path = log_dir / "prisma_decisions.jsonl"

for path in [counts_path, decisions_path]:
    if path.exists():
        path.unlink()
        print(f"Reset: {path.name}")

# Run cleaning and count scripts
subprocess.run(["python", "-m", "scripts.clean.clean_data"], check=True)
subprocess.run(["python", "-m", "scripts.analysis.count_prisma_stages"], check=True)

# Wait for prisma_counts.json to exist and be non-empty
for _ in range(20):
    if counts_path.exists() and counts_path.stat().st_size > 0:
        break
    time.sleep(0.2)
else:
    raise FileNotFoundError("prisma_counts.json not found or empty after count_prisma_stages.py")

# Generate PRISMA2020-compliant CSV
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

# Set number of clusters
n_clusters = 8

# Cluster keywords
clusters, filtered_lists = cluster_keywords(df, column="word_list", n_clusters=n_clusters, return_tokens=True)

# Assign semantic labels and color codes
cluster_names, cluster_colors = name_clusters(clusters)

print(f"Raw cluster count: {len(clusters)}")

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

# Compute layout
pos = compute_layout(G, layout_type="kamada") # spring or kamada or circular or spectral

# Render interactive map
plot_interactive(
    G,
    term_freq,
    pos,
    sizing_mode="frequency", # "frequency" or "co-occurrence"
    cluster_colors=cluster_colors,
    strong_edge_scale=0.5,
    weak_edge_scale=0.5,
    edge_threshold=0.1
)