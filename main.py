import os
import random
import subprocess
from datetime import datetime, timedelta

def run_git_command(command, env=None):
    """Executes a git shell command."""
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    if result.returncode != 0:
        print(f"Error executing command '{command}': {result.stderr.strip()}")
        return False
    return True

def generate_commits(num_commits):
    filename = "contribution_log.txt"
    
    # Ensure the target file exists
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("Git Commit Activity Log\n")

    today = datetime.now()
    one_year_ago = today - timedelta(days=365)

    print(f"\nGenerating {num_commits} backdated commits between {one_year_ago.strftime('%Y-%m-%d')} and {today.strftime('%Y-%m-%d')}...\n")

    for i in range(1, num_commits + 1):
        # Pick a random number of days and seconds ago within the past year
        random_days = random.randint(0, 365)
        random_seconds = random.randint(0, 86400)
        commit_date = today - timedelta(days=random_days, seconds=random_seconds)
        date_str = commit_date.strftime("%Y-%m-%dT%H:%M:%S")

        # Make a small change to the file
        with open(filename, "a") as f:
            f.write(f"Commit {i} - {date_str}\n")

        # Stage the file
        if not run_git_command(f"git add {filename}"):
            break

        # Set environment variables for both author and committer dates
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str

        commit_msg = f"Backdated commit #{i}"
        commit_cmd = f'git commit -m "{commit_msg}"'

        if run_git_command(commit_cmd, env=env):
            print(f"[{i}/{num_commits}] Committed on {date_str}")
        else:
            print(f"Failed at commit {i}")
            break

    print("\nFinished creating commits!")
    print("Run 'git push origin main' (or your target branch) to sync with GitHub.")

if __name__ == "__main__":
    # Ensure this directory is a git repository
    if not os.path.exists(".git"):
        print("Error: This directory is not a Git repository. Run 'git init' first.")
    else:
        try:
            commits_input = input("Enter the number of commits to generate: ")
            num_commits = int(commits_input)
            if num_commits <= 0:
                print("Please enter a positive integer.")
            else:
                generate_commits(num_commits)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
