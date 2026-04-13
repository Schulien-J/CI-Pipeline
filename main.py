import requests
import keyring
import process_handler as ph
import json

cache = {}
owner = "Schulien-J" 
projekt = "CI-Pipeline"

url = f"https://api.github.com/repos/{owner}/{projekt}/branches"

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
    
def save_cache():
    return 1
    

response = requests.get(url, headers=headers)
prs = response.json()
print(prs)

processed = load_processed()

for pr in prs:
    pr_id = str(pr["number"])
    pr_branch = pr["base"]["ref"]
    pr_branch_head = pr["base"]["sha"]
    print(pr_branch, pr_branch_head)
    if pr_id in processed:
        continue

    ph.handle_pr(int(pr_id))
    processed.add(pr_id)


save_processed(processed)
#TODO enter while loop to wait for new PRs 





#TODO ENTER Webhook loop