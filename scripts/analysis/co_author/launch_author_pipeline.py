from scripts.analysis.co_author.ris_clean import load_ris_clean
from scripts.analysis.co_author.build_author_matrix import build_author_matrix
from scripts.analysis.co_author.build_author_topics import (
    build_author_embeddings,
    cluster_author_embeddings,
    label_clusters_by_keywords
)
from scripts.analysis.co_author.cluster_author_graph import cluster_author_graph
from scripts.analysis.co_author.visualize_author_map import visualize_author_graph

def run_pipeline(ris_path="data_sources/raw/mendeley_export.ris"):
    print("Launching author pipeline...")
    parsed = load_ris_clean(ris_path)
    if not parsed:
        print("No entries parsed. Aborting.")
        return

    # Build co-authorship matrix
    matrix = build_author_matrix(parsed)

    # Embed author texts and cluster them semantically
    embeddings = build_author_embeddings(parsed)
    semantic_labels = cluster_author_embeddings(embeddings, n_clusters=6)

    # Extract top keywords per cluster and assign readable labels
    cluster_labels = label_clusters_by_keywords(parsed, semantic_labels, top_k=2)
    semantic_labels_named = {
        author: cluster_labels[cluster_id]
        for author, cluster_id in semantic_labels.items()
    }

    # Build graph and visualize with thematic labels
    G = cluster_author_graph(matrix, semantic_labels=semantic_labels_named)
    visualize_author_graph(G)
    print("G type:", type(G))