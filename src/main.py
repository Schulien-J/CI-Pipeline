import requests
import keyring
import process_handler as ph
import json

cache = {}
owner = "Schulien-J" 
projekt = "CI-Pipeline"

url = f"https://api.github.com/repos/{owner}/{projekt}/pulls"

#TODO  add your own token for personal use
token = keyring.get_password("my_ci_tool", "github_token")
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}


def load_processed(file="processed_prs.txt"):
    try:
        with open(file, "r") as f:
            return set(line.strip() for line in f if line.strip())   #this strips twice
    except FileNotFoundError:
        return set()
    
def save_processed(processed, file="processed_prs.txt"):
    with open(file, "w") as f:
        for pr in processed:
            f.write(str(pr) + "\n")

def load_cache():
    with open("branch_cache.json","r") as f:
        cache = json.load(f)
    branch_url = f"https://api.github.com/repos/{owner}/{projekt}/branches"
    branches = requests.get(branch_url,headers)
    branches = branches.json()
    
    for branch in branches:
        cache[branch["name"]] = branch["commit"]["sha"]
    return cache
    
def save_cache():
     with open("branch_cache.json","w") as f:
        json.dump(cache,f)
    

response = requests.get(url, headers=headers)
prs = response.json()
cache = load_cache()
save_cache()

processed = load_processed()

for pr in prs:
    pr_id = str(pr["number"])
    if pr_id in processed:
        continue
    pr_branch = pr["base"]["ref"]
    pr_branch_head = pr["head"]["sha"]
    ph.handle_pr(pr_branch, pr_branch_head)
    processed.add(pr_id)


save_processed(processed)
#TODO enter while loop to wait for new PRs 





#TODO ENTER Webhook loop