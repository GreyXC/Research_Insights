import matplotlib.pyplot as plt
import seaborn as sns

def plot_keyword_bar_chart(clusters, cluster_names, cluster_colors=None):
    # Flatten data for plotting
    data = []
    for cluster_id, keywords in clusters.items():
        label = cluster_names.get(cluster_id, cluster_id) if cluster_names else cluster_id
        for keyword, count in keywords:
            data.append({
                "Keyword": keyword,
                "Count": count,
                "Cluster": label
            })

    # Create DataFrame
    import pandas as pd
    df = pd.DataFrame(data)

    # Set up color palette
    cluster_order = sorted(df["Cluster"].unique())
    palette = sns.color_palette("hls", len(cluster_order))

    # Plot
    plt.figure(figsize=(18, 6))
    sns.barplot(
        data=df,
        x="Keyword",
        y="Count",
        hue="Cluster",
        palette=dict(zip(cluster_order, palette)),
        dodge=False
    )

    plt.title("Top Keywords by Theme")
    plt.xlabel("Keyword")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Cluster", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()