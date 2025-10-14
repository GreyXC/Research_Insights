import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

def plot_clusters(df, n_clusters=5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    abstracts = df["abstract"].fillna("").tolist()
    embeddings = model.encode(abstracts)

    # Reduce to 2D
    pca = PCA(n_components=2)
    components = pca.fit_transform(embeddings)

    # Cluster
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)
    df["Cluster"] = labels

    # Plot
    plt.figure(figsize=(10, 6))
    for cluster_id in sorted(df["Cluster"].unique()):
        idx = df["Cluster"] == cluster_id
        plt.scatter(
            components[idx, 0],
            components[idx, 1],
            label=f"Cluster {cluster_id}",
            alpha=0.6
        )

    plt.xlabel("Technological Change")
    plt.ylabel("Social Change")
    plt.title("Semantic Landscape of Abstracts")
    plt.legend()
    plt.tight_layout()
    plt.show()
