import pandas as pd

def parse_ris(filepath):
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    records = []
    record = {}
    for line in lines:
        if line.strip() == "":
            continue
        if line.startswith("TY  -"):
            record = {}
        elif line.startswith("ER  -"):
            records.append(record)
        else:
            tag, _, value = line.partition("  - ")
            tag = tag.strip()
            value = value.strip()
            if tag in record:
                record[tag] += "; " + value
            else:
                record[tag] = value

    df = pd.DataFrame([{
        "title": r.get("TI", ""),
        "abstract": r.get("AB", ""),
        "year": r.get("PY", ""),
        "tags": r.get("KW", "")
    } for r in records])

    return df

if __name__ == "__main__":
    print("parse_ris is importable and working.")
