import matplotlib.pyplot as plt

def plot_keywords(keywords, top_n=20):
    """
    Plots a horizontal bar chart of the top keywords.

    Parameters:
    - keywords: List of (keyword, frequency) tuples
    - top_n: Number of top keywords to display
    """
    # Select top N keywords
    top_keywords = keywords[:top_n]
    words = [kw[0] for kw in top_keywords]
    counts = [kw[1] for kw in top_keywords]

    # Plot
    plt.figure(figsize=(10, 6))
    plt.barh(words[::-1], counts[::-1], color="skyblue")
    plt.xlabel("Frequency")
    plt.title("Top Keywords in Abstracts")
    plt.tight_layout()
    plt.show()
