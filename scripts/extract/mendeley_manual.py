import requests
import os
import json

CLIENT_ID = os.getenv("MENDELEY_CLIENT_ID", "21265")
CLIENT_SECRET = os.getenv("MENDELEY_CLIENT_SECRET", "xOxlONQTqXwhMFKl")
REDIRECT_URI = "http://localhost:8080"

def get_access_token(code):
    token_url = "https://api.mendeley.com/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

def fetch_documents(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api.mendeley.com/documents?view=all&limit=500"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def extract_metadata(docs):
    metadata = []
    for doc in docs:
        entry = {
            "title": doc.get("title"),
            "authors": [a.get("last_name") for a in doc.get("authors", [])],
            "year": doc.get("year"),
            "type": doc.get("type"),
            "source": doc.get("source"),
            "keywords": doc.get("keywords"),
            "abstract": doc.get("abstract"),
        }
        metadata.append(entry)
        print(f"✅ {entry['title']}")
    return metadata

def save_metadata(metadata, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"\n📁 Saved to {path}")

if __name__ == "__main__":
    print("🔗 Authorize here:")
    print(f"https://api.mendeley.com/oauth/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=all")
    redirect_url = input("Paste the full redirect URL: ")
    code = redirect_url.split("code=")[-1].split("&")[0]
    token = get_access_token(code)
    docs = fetch_documents(token)
    metadata = extract_metadata(docs)
    save_metadata(metadata, "data_sources/raw/mendeley_metadata.json")