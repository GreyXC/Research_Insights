import seaborn as sns

def bucket_size(freq, scale=0.8):
    if freq < 3:
        return int(50 * scale)
    elif freq < 15:
        return int(200 * scale)
    else:
        return int(900 * scale)

def font_size_from_node_size(size):
    return max(6, min(16, int(size / 60)))

def get_color_map(labels):
    palette = sns.color_palette("hls", len(labels))
    return dict(zip(labels, palette))