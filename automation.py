import subprocess
import re
import os
import datetime
import yaml

def calculate_change_failure_rate(num_deployments, num_issues):
    if num_deployments <= 0:
        raise ValueError("Number of deployments must be greater than 0")

    if num_issues < 0:
        raise ValueError("Number of issues cannot be negative")

    change_failure_rate = (num_issues / num_deployments) * 100
    return round(change_failure_rate, 2)




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
total_deployments = number_of_bugs + number_of_hotfixes + number_of_features
total_issues = number_of_bugs + number_of_hotfixes
cfr = calculate_change_failure_rate(total_deployments, total_issues)
stringified_cfr = f"""{cfr} %"""

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
        release_metrics['cfr'] = stringified_cfr
        
        current_release_dict = { 'total': total_deployments, 'features': number_of_features, 'bugs': number_of_bugs, 'hotfixes': number_of_hotfixes, 'cfr': stringified_cfr }
        
        # append the current release metrics
        release_metrics[f"""release_{current_release}"""] = current_release_dict 
        
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
    .cfr = "{stringified_cfr}" |
    .total_releases = {total_releases} |
    .total_features = {number_of_features} |
    .total_bugs = {number_of_bugs} |
    .total_hotfixes = {number_of_hotfixes}
    """
    
    print(yaml_content)        
    yq_operation = f"""yq -i '{yaml_content}' metrics.yaml"""
    os.system(yq_operation)
   

