from scripts.analysis.co_author.ris_clean import load_ris_clean
from scripts.analysis.co_author.build_author_matrix import build_author_matrix
from scripts.analysis.co_author.cluster_author_graph import cluster_author_graph
from scripts.analysis.co_author.visualize_author_map import visualize_author_graph

def run_pipeline(ris_path="data_sources/raw/mendeley_export.ris"):
    print("Launching author pipeline...")
    parsed = load_ris_clean(ris_path)
    if not parsed:
        print("No entries parsed. Aborting.")
        return

    matrix = build_author_matrix(parsed)
    G = cluster_author_graph(matrix)
    visualize_author_graph(G)
    print("G type:", type(G))