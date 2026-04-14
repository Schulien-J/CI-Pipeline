import requests
import keyring
import process_handler as ph
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CACHE_FILE = BASE_DIR / "branch_cache.json"
PROCESSED_FILE = BASE_DIR / "processed_prs.txt"


cache = {}
owner = "Schulien-J" 
projekt = "CI-Pipeline"

url = f"https://api.github.com/repos/{owner}/{projekt}/pulls"

#TODO  add your own token for personal use
token = keyring.get_password("my_ci_tool", "github_token")
headerss = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

def load_processed():
    try:
        with open(PROCESSED_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())   #this strips twice
    except FileNotFoundError:
        return set()
    
def save_processed(processed):
    with open(PROCESSED_FILE, "w") as f:
        for pr in processed:
            f.write(str(pr) + "\n")

def load_cache():
    with open(CACHE_FILE,"r") as f:
        cache = json.load(f)
    branch_url = f"https://api.github.com/repos/{owner}/{projekt}/branches"
    branches = requests.get(branch_url,headers=headerss)
    branches = branches.json()
    
    for branch in branches:
        cache[branch["name"]] = branch["commit"]["sha"]
    return cache
    
def save_cache(cache):
     with open(CACHE_FILE,"w") as f:
        json.dump(cache,f)

def send_feedback(status: str, pr: str):
    payload = {
    "state": status,   
    "context": "Test " + status,
    "description": status
    } 
    feedback_url = f"https://api.github.com/repos/{owner}/{projekt}/statuses/{pr}"
    response = requests.post(feedback_url,headers=headerss,json=payload)
    print(response.status_code)
    print(response.text)
    
def main():
    response = requests.get(url, headers=headerss)
    prs = response.json()
    cache = load_cache()
    save_cache(cache)

    processed = load_processed()

    for pr in prs:
        pr_id = str(pr["number"])
        if pr_id in processed:
            continue
        pr_branch = pr["base"]["ref"]
        pr_branch_head = pr["head"]["sha"]
        result = ph.handle_pr(pr_branch, pr_branch_head)
        if result == 1:
            send_feedback("success",pr_branch_head)
        else:
            send_feedback("failure",pr_branch_head)
        processed.add(pr_id)

    save_processed(processed)
    return 8


if __name__ == "__main__":
    main()

#TODO ENTER Webhook loop