def name_clusters(clusters):
    labels = {}
    colors = {}

    palette = {
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

    for cluster_id, keywords in clusters.items():
        terms = [kw.lower() for kw, _ in keywords]

        if any(t in terms for t in [
            "resilience", "policy", "governance", "equity", "justice", "participation",
            "decision-making", "institutional", "framework", "regulation"
        ]):
            label = "Governance & Equity"

        elif any(t in terms for t in [
            "flood", "infrastructure", "landslide", "critical", "risk", "disaster",
            "vulnerability", "adaptation", "earthquake", "storm", "hazard"
        ]):
            label = "Infrastructure Risk & Resilience"

        elif any(t in terms for t in [
            "food", "service", "development", "access", "health", "education",
            "basic services", "livelihood", "housing", "nutrition", "welfare"
        ]):
            label = "Sustainable Systems & Access"

        elif any(t in terms for t in [
            "urban", "freight", "gis", "planning", "spatial", "zoning", "mapping",
            "open data", "smart city", "land use", "urban design"
        ]):
            label = "Urban Planning & Open Data"

        elif any(t in terms for t in [
            "crisis", "communication", "modeling", "game", "simulation", "scenario",
            "response", "preparedness", "emergency", "coordination", "alert"
        ]):
            label = "Crisis Modeling & Communication"

        elif any(t in terms for t in [
            "mobility", "delivery", "transport", "logistics", "last mile", "routing",
            "distribution", "vehicle", "fleet", "traffic", "modal"
        ]):
            label = "Urban Logistics & Mobility"

        elif any(t in terms for t in [
            "data", "simulation", "model", "network", "algorithm", "machine learning",
            "optimization", "system", "architecture", "computational", "digital twin"
        ]):
            label = "Computational Modeling & Systems"

        elif any(t in terms for t in [
            "air", "pollution", "region", "hazard", "wildfire", "emissions",
            "toxicity", "exposure", "geographic", "environmental health"
        ]):
            label = "Regional Environmental Hazards"

        else:
            top_term = terms[0].title() if terms else "Unknown"
            label = f"Theme: {top_term}"

        labels[cluster_id] = label
        colors[label] = palette.get(label, palette["Fallback"])

    return labels, colors