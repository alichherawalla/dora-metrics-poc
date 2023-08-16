import subprocess
import re
import os
import datetime

# Run git log command to get merge commit messages
git_log_command = "git log --oneline origin/main..origin/dev"
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

# Read the existing metrics.yaml content
target_yaml_file = "metrics.yaml"
with open(target_yaml_file, "r") as file:
    existing_yaml_content = file.read()

# Update total_releases based on the number of release sections
total_releases = existing_yaml_content.count("release_")
new_release_number = total_releases + 1

# Generate the release YAML content for the new release
new_release_yaml = f"""
release_{new_release_number}:
  bugs: {new_release_number * 2}
  features: {new_release_number * 10}
  hotfixes: {new_release_number}
"""

# Update the total_releases value
updated_yaml_content = existing_yaml_content.replace(
    f"total_releases: {total_releases}",
    f"total_releases: {new_release_number}"
)

# Add the new release YAML content
updated_yaml_content = updated_yaml_content.replace("# release_2:", new_release_yaml, 1)

# Write the updated content back to metrics.yaml
with open(target_yaml_file, "w") as file:
    file.write(updated_yaml_content)

# Commit the changes to the current branch
subprocess.run(["git", "add", target_yaml_file])
subprocess.run(["git", "commit", "-m", "Update metrics.yml file"])