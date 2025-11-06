import pandas as pd
from collections import defaultdict
import itertools

def build_author_matrix(entries):
    coauthor_counts = defaultdict(lambda: defaultdict(int))
    for entry in entries:
        authors = entry.get('authors', [])
        for a1, a2 in itertools.combinations(sorted(set(authors)), 2):
            coauthor_counts[a1][a2] += 1
            coauthor_counts[a2][a1] += 1
    df = pd.DataFrame(coauthor_counts).fillna(0).astype(int)
    return df