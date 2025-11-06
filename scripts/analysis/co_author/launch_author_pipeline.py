def run_pipeline(ris_path="../../data_sources/raw/mendeley_export.ris"):
    from ris_clean import load_ris_clean
    from build_author_matrix import build_author_matrix
    from cluster_author_graph import cluster_author_graph
    from visualize_author_map import visualize_author_graph

    parsed = load_ris_clean(ris_path)
    if not parsed:
        print("No entries parsed. Aborting.")
        return

    matrix = build_author_matrix(parsed)
    G = cluster_author_graph(matrix)
    visualize_author_graph(G)
    print("G type:", type(G))