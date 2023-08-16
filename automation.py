import subprocess
import re

# Run git log command to get merge commit messages
git_log_command = "git log --oneline origin/main...origin/dev"
merge_commits = subprocess.check_output(git_log_command, shell=True, text=True).splitlines()

# Regular expressions for categorization
feature_pattern = re.compile(r'Merge pull request #(\d+) from .*\/(feat|chore|docs)\/.*')
bug_pattern = re.compile(r'Merge pull request #(\d+) from .*\/(fix|bug)\/.*')
hotfix_pattern = re.compile(r'Merge pull request #(\d+) from .*\/hotfix\/.*')

# Categorize messages
feature_messages = []
bug_messages = []
hotfix_messages = []

for message in merge_commits:
    if re.search(feature_pattern, message):
        feature_messages.append(message)
    elif re.search(bug_pattern, message):
        bug_messages.append(message)
    elif re.search(hotfix_pattern, message):
        hotfix_messages.append(message)

# Print the categorized messages
print("Feature Messages:")
print(len(feature_messages))
print("Bug Messages:")
print(len(bug_messages))
print("Hotfix Messages:")
print(len(hotfix_messages))