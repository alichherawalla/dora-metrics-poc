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

# Generate the YAML content for releases
release_yaml = ""
for release_number in range(1, 4):  # Assuming three releases
    release_yaml += f"""
release_{release_number}:
  bugs: {release_number * 2}
  features: {release_number * 10}
  hotfixes: {release_number}
"""

# Generate the overall YAML content
yaml_content = f"""
cfr: 0
total_releases: 3  # Update this number based on the actual number of releases
total_features: {len(feature_messages)}
total_bugs: {len(bug_messages)}
total_hotfixes: {len(hotfix_messages)}

{release_yaml}
"""

# Path to the target YAML file
target_yaml_file = "metrics.yaml"

# Write the YAML content to a temporary file
temp_yaml_file = "temp_metrics.yaml"
with open(temp_yaml_file, "w") as file:
    file.write(yaml_content)

# Use yq to update the target YAML file in place
subprocess.run(["yq", "eval", "-i", f". = import('{temp_yaml_file}')", target_yaml_file])

# Remove the temporary file
os.remove(temp_yaml_file)

# Commit the changes to the current branch
subprocess.run(["git", "add", target_yaml_file])
subprocess.run(["git", "commit", "-m", "Update metrics.yml file"])
import subprocess
import re
import os
import datetime
import yaml

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

# Path to the target YAML file
target_yaml_file = "metrics.yaml"

# Check if the metrics file exists
if os.path.exists(target_yaml_file):
    # Read the existing YAML content
    with open(target_yaml_file, "r") as yaml_file:
        existing_yaml = yaml.safe_load(yaml_file)
    
    # Determine the number of releases from the existing YAML content
    total_releases = existing_yaml.get("total_releases", 0)
    
    # Generate the YAML content for releases
    release_yaml = ""
    for release_number in range(1, total_releases + 1):
        release_info = existing_yaml.get(f"release_{release_number}", {})
        release_yaml += f"""
release_{release_number}:
  bugs: {release_info.get("bugs", 0)}
  features: {release_info.get("features", 0)}
  hotfixes: {release_info.get("hotfixes", 0)}
"""
else:
    total_releases = 0
    release_yaml = ""

# Generate the overall YAML content
yaml_content = f"""
cfr: 0
total_releases: {total_releases}
total_features: {len(feature_messages)}
total_bugs: {len(bug_messages)}
total_hotfixes: {len(hotfix_messages)}

{release_yaml}
"""

# Write the updated YAML content
with open(target_yaml_file, "w") as file:
    file.write(yaml_content)

# Commit the changes to the current branch
subprocess.run(["git", "add", target_yaml_file])
subprocess.run(["git", "commit", "-m", "Update metrics.yml file"])
