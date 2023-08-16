import re
import os
import subprocess
import git

def get_recent_merge_commit(repo, branch_name):
    try:
        command = ["git", "rev-list", "-n", "1", "--merges", branch_name]
        result = subprocess.run(command, cwd=repo.working_dir, stdout=subprocess.PIPE, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_commit_messages(repo, from_commit, to_commit):
    try:
        commits = repo.iter_commits(f"{from_commit}..{to_commit}")
        # commits = repo.iter_commits(from_commit)
        commit_messages = [commit.message.strip() for commit in commits]
        return commit_messages
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    try:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        repo = git.Repo(current_directory)
        main_branch_name = "main"

        recent_merge_commit = get_recent_merge_commit(repo, main_branch_name)
        if recent_merge_commit is None:
            print("No recent merge commit found.")
            return

        commit_messages = get_commit_messages(repo, main_branch_name, recent_merge_commit)
        print(commit_messages)
        num_changes = len(commit_messages)

        print(f"Number of changes in the recent merge pull request: {num_changes}")
        for i, message in enumerate(commit_messages, start=1):
            print(f"Change {i}: {message}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
