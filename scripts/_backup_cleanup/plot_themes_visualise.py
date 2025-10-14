import matplotlib.pyplot as plt

def plot_theme_clusters(themes_dict):
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.tab10.colors
    bar_width = 0.2

    all_keywords = []
    all_freqs = []
    all_positions = []
    all_labels = []
    theme_offsets = {}

    # Calculate positions
    for i, (theme, words) in enumerate(themes_dict.items()):
        keywords = [w for w, _ in words]
        freqs = [c for _, c in words]
        positions = [x + i * bar_width for x in range(len(keywords))]
        all_keywords.extend(keywords)
        all_freqs.extend(freqs)
        all_positions.extend(positions)
        all_labels.extend([theme] * len(keywords))
        theme_offsets[theme] = i

        ax.bar(positions, freqs, width=bar_width, label=theme, color=colors[i % len(colors)])
        for j, kw in enumerate(keywords):
            ax.text(positions[j], freqs[j] + 0.5, kw, ha="center", fontsize=8, rotation=90)

    ax.set_title("Keyword Frequencies by Theme")
    ax.set_ylabel("Frequency")
