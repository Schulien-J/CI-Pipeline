import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
TEST_DIR = BASE_DIR / "tests"
print(TEST_DIR)

def run(cmd,path):
    result = subprocess.run(cmd, cwd=path, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return result.stdout



def handle_pr(pr_branch: str, pr_head: str, remote="origin"):
    
    run(["git", "fetch", remote], SRC_DIR)
    run(["git", "checkout", pr_branch], SRC_DIR)
    run(["git", "reset", "--hard", f"{remote}/{pr_branch}"], SRC_DIR)

    result = subprocess.run(
        ["git", "merge", pr_head],
        SRC_DIR,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return False
    result = run(["PYTHONPATH=src", "python3","-m","pytest"],TEST_DIR)
    if result == 0:
        return True
    else:
        return False
    

