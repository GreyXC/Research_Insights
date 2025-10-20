import pandas as pd
from scripts.load.load_json import load_mendeley_json
from scripts.analysis.cluster_keywords import cluster_keywords
from scripts.visualize.plot_keywords import plot_keyword_bar_chart
from scripts.visualize.plot_vosmap import plot_vos_map

def name_clusters(clusters):
    labels = {}
    for cluster_id, keywords in clusters.items():
        terms = [kw.lower() for kw, _ in keywords]

        if any(t in terms for t in [
            "resilience", "policy", "governance", "equity", "justice", "participation",
            "decision-making", "institutional", "framework", "regulation"
        ]):
            labels[cluster_id] = "Governance & Equity"

        elif any(t in terms for t in [
            "flood", "infrastructure", "landslide", "critical", "risk", "disaster",
            "vulnerability", "adaptation", "earthquake", "storm", "hazard"
        ]):
            labels[cluster_id] = "Infrastructure Risk & Resilience"

        elif any(t in terms for t in [
            "food", "service", "development", "access", "health", "education",
            "basic services", "livelihood", "housing", "nutrition", "welfare"
        ]):
            labels[cluster_id] = "Sustainable Systems & Access"

        elif any(t in terms for t in [
            "urban", "freight", "gis", "planning", "spatial", "zoning", "mapping",
            "open data", "smart city", "land use", "urban design"
        ]):
            labels[cluster_id] = "Urban Planning & Open Data"

        elif any(t in terms for t in [
            "crisis", "communication", "modeling", "game", "simulation", "scenario",
            "response", "preparedness", "emergency", "coordination", "alert"
        ]):
            labels[cluster_id] = "Crisis Modeling & Communication"

        elif any(t in terms for t in [
            "mobility", "delivery", "transport", "logistics", "last mile", "routing",
            "distribution", "vehicle", "fleet", "traffic", "modal"
        ]):
            labels[cluster_id] = "Urban Logistics & Mobility"

        elif any(t in terms for t in [
            "data", "simulation", "model", "network", "algorithm", "machine learning",
            "optimization", "system", "architecture", "computational", "digital twin"
        ]):
            labels[cluster_id] = "Computational Modeling & Systems"

        elif any(t in terms for t in [
            "air", "pollution", "region", "hazard", "wildfire", "emissions",
            "toxicity", "exposure", "geographic", "environmental health"
        ]):
            labels[cluster_id] = "Regional Environmental Hazards"

        else:
            top_term = terms[0].title() if terms else "Unknown"
            labels[cluster_id] = f"Theme: {top_term}"

    return labels

def run_pipeline():
    print("Loading Mendeley metadata...")
    df = load_mendeley_json("data_sources/raw/mendeley_metadata.json")
    print(f"Loaded {len(df)} entries.")

    print("\nClustering keywords from abstracts...")
    clusters = cluster_keywords(df, column="abstract")
    print(f"Identified {len(clusters)} keyword clusters.")

    print("\nAssigning cluster names...")
    cluster_names = name_clusters(clusters)
    for label, name in cluster_names.items():
        print(f"{label}: {name}")

    print("\nGenerating bar chart...")
    plot_keyword_bar_chart(clusters, cluster_names)

    print("\nGenerating VOS-style map...")
    plot_vos_map(clusters, cluster_names)

if __name__ == "__main__":
    run_pipeline()