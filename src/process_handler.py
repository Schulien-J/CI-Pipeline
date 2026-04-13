import subprocess

def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return result.stdout



def handle_pr(pr_branch: str, pr_head: str, remote="origin"):
    
    run(["git", "fetch", remote])
    run(["git", "checkout", pr_branch])
    run(["git", "reset", "--hard", f"{remote}/{pr_branch}"])

    result = subprocess.run(
        ["git", "merge", pr_head],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False
    return True

