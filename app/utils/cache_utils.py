import json, os

CACHE_DIR = ".cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def cache_repo_summary(repo_name, summary):
    path = os.path.join(CACHE_DIR, f"{repo_name}.json")
    with open(path, "w") as f:
        json.dump(summary, f)

def load_cached_summary(repo_name):
    path = os.path.join(CACHE_DIR, f"{repo_name}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None
