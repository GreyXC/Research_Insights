def name_clusters(clusters):
    from collections import Counter

    labels = {}
    colors = {}

    # Predefined theme colors
    palette = {
        "Community-Centered Logistics & Access": "#FF7F0E",
        "Hybrid Automation & Micro-Mobility Systems": "#1F77B4",
        "Urban Mid-Block Morphology": "#2CA02C",
        "Governance, Planning & Open Systems": "#9467BD",
        "Infrastructure Risk & Spatial Interference": "#AA0D0D",
        "Computational Modeling & Responsive Systems": "#F87B62",
        "Environmental Integration & Urban Sustainability": "#E377C2",
        "Emerging CLuster": "#7F7F7F"
    }

    # Expanded theme keyword sets
    theme_keywords = {
        "Community-Centered Logistics & Access": {
            "community", "access", "delivery", "service", "shared", "inclusive",
            "last mile", "neighborhood", "participation", "livelihood",
            "public service", "micro-logistics", "local", "hub", "pickup", "drop-off"
        },
        "Hybrid Automation & Micro-Mobility Systems": {
            "automated", "hybrid", "robotics", "micro-mobility", "autonomous",
            "vehicle", "fleet", "routing", "cycle", "cargo", "driver",
            "ride-hailing", "platform", "dispatch", "navigation", "sensor"
        },
        "Urban Mid-Block Morphology": {
            "mid-block", "urban", "block", "space", "vacant", "underused",
            "activation", "redevelopment", "density", "built environment",
            "land use", "spatial", "zoning", "urban design", "public space",
            "interstitial", "alley", "courtyard", "passage", "threshold"
        },
        "Governance, Planning & Open Systems": {
            "governance", "policy", "planning", "regulation", "framework",
            "open data", "smart city", "participation", "decision-making",
            "institutional", "transparency", "stakeholder", "accessibility",
            "urban planning", "city planning", "adaptive", "resilience"
        },
        "Infrastructure Risk & Spatial Interference": {
            "interference", "conflict", "risk", "resilience", "vulnerability",
            "disruption", "hazard", "traffic", "congestion", "storm", "flood",
            "critical", "adaptation", "mitigation", "safety", "pedestrian",
            "collision", "obstruction", "visibility", "navigation"
        },
        "Computational Modeling & Responsive Systems": {
            "data", "model", "simulation", "network", "algorithm", "ai",
            "machine learning", "optimization", "digital twin", "computational",
            "predictive", "responsive", "system", "architecture", "pipeline",
            "feedback", "sensor", "real-time", "analytics"
        },
        "Environmental Integration & Urban Sustainability": {
            "climate", "pollution", "air", "emissions", "toxicity", "exposure",
            "green", "sustainable", "ecosystem", "environmental health",
            "urban ecology", "heat", "drought", "wildfire", "contamination",
            "environmental hazard", "atmospheric", "low-carbon", "energy"
        }
    }

    used_labels = set()

    for cluster_id, keywords in clusters.items():
        terms = [kw.lower() for kw, _ in keywords]
        top_terms = terms[:5]
        term_set = set(terms)

        # Weighted theme scoring
        best_match = None
        best_score = 0
        for theme, theme_terms in theme_keywords.items():
            score = sum(2 if t in top_terms else 1 for t in term_set if t in theme_terms)
            if score > best_score:
                best_match = theme
                best_score = score

        # Assign theme if score is strong enough
        if best_match and best_score >= 2:
            label = best_match
        else:
            fallback_terms = [kw for kw in top_terms if kw.isalpha()]
            label = f"Emergent Theme: {' / '.join(fallback_terms[:1])}"

            # Ensure uniqueness
            while label in used_labels:
                fallback_terms = fallback_terms[1:] + [kw for kw in terms[len(fallback_terms):len(fallback_terms)+1]]
                label = f"Emergent Theme: {' / '.join(fallback_terms[:1])}"

            print(f"⚠️ Fallback label used for Cluster {cluster_id}: {label}")

        labels[cluster_id] = label

        # Assign color
        if label in palette:
            colors[label] = palette[label]
        else:
            # Assign a distinct fallback color
            fallback_color = "#999999"
            colors[label] = fallback_color

        used_labels.add(label)

        # Optional debug log
        print(f"Cluster {cluster_id} → {label} (score: {best_score})")

    return labels, colors