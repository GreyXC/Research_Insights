import rispy

def load_ris_clean(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        entries = rispy.load(f)
    for entry in entries:
        entry['authors'] = entry.get('authors', [])
    return entries