import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_theme_clusters(themes_dict):
    # Prepare data
    data = []
    for theme, words in themes_dict.items():
        for word, count in words:
            data.append({"Theme": theme, "Keyword": word, "Frequency": count})
    df = pd.DataFrame(data)

    # Set Seaborn style
    sns.set(style="whitegrid")

    # Create plot
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=df, x="Keyword", y="Frequency", hue="Theme", dodge=True)

    # Rotate x labels and format
    plt.xticks(rotation=45, ha="right")
    plt.title("Keyword Frequencies by Theme")
    plt.ylabel("Frequency")
    plt.xlabel("Keyword")
    plt.legend(title="Theme")
    plt.tight_layout()
    plt.show()
