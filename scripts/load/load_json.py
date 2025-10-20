import pandas as pd
import json

def load_mendeley_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)