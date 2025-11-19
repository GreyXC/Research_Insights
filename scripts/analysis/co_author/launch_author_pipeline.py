from scripts.analysis.co_author.ris_clean import load_ris_clean
from scripts.analysis.co_author.build_author_matrix import build_author_matrix
from scripts.analysis.co_author import build_author_topics as bat
from scripts.analysis.co_author.cluster_author_graph import cluster_author_graph
from scripts.analysis.co_author.visualize_author_map import visualize_author_graph

def run_pipeline(ris_path="data_sources/raw/mendeley_export.ris"):
    print("Launching author pipeline...")
    parsed = load_ris_clean(ris_path)
    if not parsed:
        print("No entries parsed. Aborting.")
        return

    matrix = build_author_matrix(parsed)
    embeddings = bat.build_author_embeddings(parsed)
    semantic_labels = bat.cluster_author_embeddings(embeddings, n_clusters=6)
    cluster_labels = bat.label_clusters_by_keywords(parsed, semantic_labels, top_k=2)
    semantic_labels_named = {
        author: cluster_labels[cluster_id]
        for author, cluster_id in semantic_labels.items()
    }

    G = cluster_author_graph(matrix, semantic_labels=semantic_labels_named)

    # Inject scaled PCA layout seed
    pca_coords = bat.project_embeddings_pca(embeddings)
    scaled_coords = {author: (x * 5.0, y * 5.0) for author, (x, y) in pca_coords.items()}
    for author, (x, y) in scaled_coords.items():
        if author in G.nodes:
            G.nodes[author]['layout_seed'] = (x, y)

    visualize_author_graph(G)
    print("G type:", type(G))

if __name__ == "__main__":
    run_pipeline()