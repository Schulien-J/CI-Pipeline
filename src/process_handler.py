import subprocess
from pathlib import Path
import tempfile
import os
import sys

repo = "https://github.com/Schulien-J/Monitored-by-CI-Pipeline.git"

def handle_pr(pr_branch: str, pr_head: str, remote="origin"):
    with tempfile.TemporaryDirectory() as repo_dir:
        subprocess.run(["git", "clone", repo, repo_dir],check=True)
        subprocess.run(["git", "fetch", "origin"],cwd=repo_dir,check=True)
        subprocess.run(["git", "checkout", pr_branch],cwd=repo_dir,check=True)
        merge_result = subprocess.run(["git", "merge", "--no-edit", pr_head],cwd=repo_dir)
        if merge_result.returncode != 0:
            return False  
        
        venv_dir = os.path.join(repo_dir, ".venv")     
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

        venv_python = os.path.join(venv_dir, "bin", "python")
        venv_pip    = os.path.join(venv_dir, "bin", "pip")
        req_file = os.path.join(repo_dir, "requirements.txt")

        if os.path.exists(req_file):
            subprocess.run([venv_pip, "install", "-r", req_file],check=True)
        else:
            return 0 #ERROR

        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.join(repo_dir, "src")  
        test_result = subprocess.run([venv_python, "-m", "pytest"],cwd=repo_dir,env=env) 
        return test_result.returncode == 0
    

