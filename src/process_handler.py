import subprocess
from pathlib import Path
import tempfile
import os

repo = "https://github.com/Schulien-J/Monitored-by-CI-Pipeline.git"

def handle_pr(pr_branch: str, pr_head: str, remote="origin"):
    with tempfile.TemporaryDirectory() as tmp_dir:
        subprocess.run(
            ["git", "clone", repo, tmp_dir],
            check=True
        )
        repo_dir = tmp_dir
        subprocess.run(
            ["git", "fetch", "origin"],
            cwd=repo_dir,
            check=True
        )
        subprocess.run(
            ["git", "checkout", pr_branch],
            cwd=repo_dir,
            check=True
        )
        merge_result = subprocess.run(
            ["git", "merge", "--no-edit", pr_head],
            cwd=repo_dir
        )
        if merge_result.returncode != 0:
            return False  

        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.join(repo_dir, "src")  
        test_result = subprocess.run(
            ["python3", "-m", "pytest"],
            cwd=repo_dir,
            env=env
        )
        return test_result.returncode == 0
    

