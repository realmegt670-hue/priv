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

def parse_date(date_str):
    """Parses date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        return None

def generate_commits(start_date, end_date, num_commits):
    filename = "contribution_log.txt"
    
    # Ensure the target file exists
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("Git Commit Activity Log\n")

    # Calculate total seconds between start and end date
    time_delta = end_date - start_date
    total_seconds = int(time_delta.total_seconds())

    if total_seconds <= 0:
        print("Error: End date must be after start date.")
        return

    print(f"\nGenerating {num_commits} commits between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}...\n")

    for i in range(1, num_commits + 1):
        # Generate a random timestamp within the specified date range
        random_seconds = random.randint(0, total_seconds)
        commit_date = start_date + timedelta(seconds=random_seconds)
        date_str = commit_date.strftime("%Y-%m-%dT%H:%M:%S")

        # Append entry to the file
        with open(filename, "a") as f:
            f.write(f"Custom Commit {i} - {date_str}\n")

        # Stage file
        if not run_git_command(f"git add {filename}"):
            break

        # Set environment variables for backdating
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str

        commit_msg = f"Custom backdated commit #{i}"
        commit_cmd = f'git commit -m "{commit_msg}"'

        if run_git_command(commit_cmd, env=env):
            print(f"[{i}/{num_commits}] Committed on {date_str}")
        else:
            print(f"Failed at commit {i}")
            break

    print("\nFinished creating custom commits!")
    print("Run your push command to update GitHub.")

if __name__ == "__main__":
    if not os.path.exists(".git"):
        print("Error: This directory is not a Git repository. Run 'git init' first.")
    else:
        print("=== Custom Date Range Commit Generator ===")
        start_input = input("Enter start date (YYYY-MM-DD): ")
        end_input = input("Enter end date (YYYY-MM-DD): ")
        
        start_date = parse_date(start_input)
        end_date = parse_date(end_input)

        if not start_date or not end_date:
            print("Invalid date format. Please use YYYY-MM-DD.")
        elif start_date >= end_date:
            print("Start date must be earlier than end date.")
        else:
            try:
                commits_input = input("Enter the number of commits to generate: ")
                num_commits = int(commits_input)
                if num_commits <= 0:
                    print("Please enter a positive integer.")
                else:
                    generate_commits(start_date, end_date, num_commits)
            except ValueError:
                print("Invalid number input.")