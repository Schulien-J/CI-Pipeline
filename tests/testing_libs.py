import json 

cache = {}
with open("branch_cache.json", "r") as f:
    cache = json.load(f)

print(cache)