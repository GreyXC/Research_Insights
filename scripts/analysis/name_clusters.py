def name_clusters(clusters):
    labels = {}
    colors = {}

    # Predefined theme colors
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

    # Expanded theme keyword sets
    theme_keywords = {
        "Governance & Equity": {
            "governance", "equity", "justice", "policy", "participation",
            "decision-making", "institutional", "framework", "regulation", "rights"
        },
        "Infrastructure Risk & Resilience": {
            "flood", "infrastructure", "landslide", "critical", "risk", "disaster",
            "vulnerability", "adaptation", "earthquake", "storm", "hazard", "resilience"
        },
        "Sustainable Systems & Access": {
            "food", "service", "development", "access", "health", "education",
            "basic services", "livelihood", "housing", "nutrition", "welfare", "water", "energy"
        },
        "Urban Planning & Open Data": {
            "urban", "freight", "gis", "planning", "spatial", "zoning", "mapping",
            "open data", "smart city", "land use", "urban design", "public space"
        },
        "Crisis Modeling & Communication": {
            "crisis", "communication", "modeling", "game", "simulation", "scenario",
            "response", "preparedness", "emergency", "coordination", "alert", "warning"
        },
        "Urban Logistics & Mobility": {
            "mobility", "delivery", "transport", "transportation", "logistics", "last mile",
            "routing", "distribution", "vehicle", "fleet", "traffic", "modal", "cycle",
            "cargo", "driver", "hub", "road", "transit"
        },
        "Computational Modeling & Systems": {
            "data", "simulation", "model", "network", "algorithm", "machine learning",
            "optimization", "system", "architecture", "computational", "digital twin", "ai"
        },
        "Regional Environmental Hazards": {
            "air", "pollution", "region", "hazard", "wildfire", "emissions",
            "toxicity", "exposure", "geographic", "environmental health", "climate"
        }
    }

    # Optional manual overrides
    manual_overrides = {
        # Example: 3: "Urban Logistics & Mobility"
    }

    used_labels = set()

    for cluster_id, keywords in clusters.items():
        terms = [kw.lower() for kw, _ in keywords]
        top_terms = terms[:5]
        term_set = set(terms)

        # Manual override
        if cluster_id in manual_overrides:
            label = manual_overrides[cluster_id]
        else:
            # Weighted theme scoring
            best_match = None
            best_score = 0
            for theme, theme_terms in theme_keywords.items():
                score = sum(2 if t in top_terms else 1 for t in term_set if t in theme_terms)
                if score > best_score:
                    best_match = theme
                    best_score = score

            # Assign theme if score is strong enough
            if best_match and best_score >= 4:
                label = best_match
            else:
                fallback_terms = [kw for kw in top_terms if kw.isalpha()]
                label = f"Theme: {'/'.join(fallback_terms[:3])}"

                # Ensure uniqueness
                while label in used_labels:
                    fallback_terms = fallback_terms[1:] + [kw for kw in terms[len(fallback_terms):len(fallback_terms)+1]]
                    label = f"Theme: {'/'.join(fallback_terms[:3])}"

        labels[cluster_id] = label
        colors[label] = palette.get(label, palette["Fallback"])
        used_labels.add(label)

        # Optional debug logging
        print(f"Cluster {cluster_id} → {label} (score: {best_score})")

    return labels, colors