import subprocess
import re
import os
import datetime
import yaml
import json

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

number_of_features = len(feature_messages)
number_of_bugs = len(feature_messages)
number_of_hotfixes = len(feature_messages)
total = number_of_bugs + number_of_hotfixes + number_of_features

if os.path.exists(target_yaml_file):
    print("Found existing metrics.yml, updating it with the latest release...")
    
    # Read the existing YAML content
    with open(target_yaml_file, "r") as yaml_file:
        release_metrics = yaml.safe_load(yaml_file)
        total_releases = release_metrics.get('total_releases')
        total_features = release_metrics.get('total_features')
        total_bugs = release_metrics.get('total_bugs')
        total_hotfixes = release_metrics.get('total_hotfixes')
        current_release = int(total_releases) + 1
        current_features = int(total_features) + 1
        current_bugs = int(total_bugs) + 1
        current_hotfixes = int(total_hotfixes) + 1
        
        release_metrics['total_releases'] = current_release
        release_metrics['total_features'] = current_features
        release_metrics['total_bugs'] = current_bugs
        release_metrics['total_hotfixes'] = current_hotfixes

        current_release_dict = { 'total': total, 'features': number_of_features, 'bugs': number_of_bugs, 'hotfixes': number_of_hotfixes }
        
        # append the current release metrics
        release_metrics[f"""release_{current_release + 1}"""] = current_release_dict 
        print(release_metrics)
        
        output_string = ""
        for outer_key, outer_value in release_metrics.items():
            if isinstance(outer_value, dict):
                # TODO: optimise this with recusion or any better algorithm
                for inner_key, inner_value in outer_value.items():
                    if isinstance(inner_value, str):
                        output_string += f""".{outer_key}.{inner_key} = "{inner_value}" | """
                    else:
                        output_string += f".{outer_key}.{inner_key} = {inner_value} | "
            else:
                if isinstance(outer_value, str):
                    output_string += f""".{outer_key} = "{outer_value}" | """
                else:
                    output_string += f".{outer_key} = {outer_value} | "
        if output_string.endswith(" | "):
            output_string = output_string[:-3]

        yq_operation = f"""yq -i '{output_string}' metrics.yaml"""
        os.system(yq_operation)
            
else:
    print('Metrics file does not exist, creating one...')
    total_releases = 1    
    
    # create the yaml file
    with open(target_yaml_file, 'w') as fp:
        pass
    yaml_content = f"""
    .cfr = "0%" |
    .total_releases = {total_releases} |
    .total_features = {number_of_features} |
    .total_bugs = {number_of_bugs} |
    .total_hotfixes = {number_of_hotfixes}
    """
        
    yq_operation = f"""yq -i '{yaml_content}' metrics.yaml"""
    os.system(yq_operation)
   

# Check if the metrics file exists
# if os.path.exists(target_yaml_file):
#     # Read the existing YAML content
#     with open(target_yaml_file, "r") as yaml_file:
#         existing_yaml = yaml.safe_load(yaml_file)
    
#     # Determine the number of releases from the existing YAML content
#     total_releases = existing_yaml.get("total_releases", 0)
    
#     # Generate the YAML content for releases
#     release_yaml = ""
#     for release_number in range(1, total_releases + 1):
#         release_info = existing_yaml.get(f"release_{release_number}", {})
#         release_yaml += f"""
# release_{release_number}:
#   bugs: {release_info.get("bugs", 0)}
#   features: {release_info.get("features", 0)}
#   hotfixes: {release_info.get("hotfixes", 0)}
# """
# else:
#     total_releases = 0
#     release_yaml = ""

# # Generate the overall YAML content
# yaml_content = f"""
# cfr: 0
# total_releases: {total_releases}
# total_features: {len(feature_messages)}
# total_bugs: {len(bug_messages)}
# total_hotfixes: {len(hotfix_messages)}

# {release_yaml}
# """

# # Write the updated YAML content
# with open(target_yaml_file, "w") as file:
#     file.write(yaml_content)

# # Commit the changes to the current branch
# subprocess.run(["git", "add", target_yaml_file])
# subprocess.run(["git", "commit", "-m", "Update metrics.yml file"])


# b = f"""
# yq -i '
#   .cfr = "25%" |
#   .total_releases = "4" |
#   .total_features = "13" |
#   .total_bugs = "6" |
#   .total_hotfixes = "6" |
#   .release_1.features = "4" |
#   .release_1.bugs = "0" |
#   .release_1.hotfixes = "1" |
#   .release_1.deployments = "5" |
#   .release_2.features = "5" |
#   .release_2.bugs = "2" |
#   .release_2.hotfixes = "0" |
#   .release_2.deployments = "0" 
# ' metrics.yaml
# """