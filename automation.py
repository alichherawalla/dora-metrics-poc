import subprocess
import re
import os

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

# Generate the YAML content using yq
yaml_content = f"""
cfr: 0
total_releases: 0
total_features: {len(feature_messages)}
total_bugs: {len(bug_messages)}
total_hotfixes: {len(hotfix_messages)}
"""

for release_number in range(1, 4):  # Assuming three releases
    yaml_content += f"""
release_{release_number}:
  bugs: {release_number * 2}
  features: {release_number * 10}
  hotfixes: {release_number}
"""

target_yaml_file = "metrics.yaml"  # Replace with the actual path

with open(target_yaml_file, "w") as file:
    file.write(yaml_content)


    # Use yq to update the target YAML file
    # subprocess.run(["yq", "eval", "-i", f". = import('{target_yaml_file}')", target_yaml_file])

# Commit the changes to the current branch
subprocess.run(["git", "add", target_yaml_file])
subprocess.run(["git", "commit", "-m", "Update metrics.yml file"])
