
import subprocess
import re
import os
import datetime
import yaml

def get_current_date():
    today = datetime.date.today()
    formatted_date = today.strftime("%d-%m-%Y")
    return formatted_date # '17-08-2023'

def calculate_change_failure_rate(num_deployments, num_issues):
    if num_deployments <= 0:
        raise ValueError("Number of deployments must be greater than 0")

    if num_issues < 0:
        raise ValueError("Number of issues cannot be negative")

    change_failure_rate = (num_issues / num_deployments) * 100
    return round(change_failure_rate, 2) # 22.12


def identify_commits():
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
    return feature_messages, bug_messages, hotfix_messages

# data.yaml
def calculate_metrics(target_data_file = 'metrics/data.yaml'):
    if os.path.exists(target_data_file):
        print("Found existing target file, updating it with the latest release...")
        
        # Read the existing YAML content
        with open(target_data_file, "r") as yaml_file:
            release_metrics = yaml.safe_load(yaml_file)
            total_releases = release_metrics.get('total_releases')
            total_features = release_metrics.get('total_feature_releases')
            total_bugs = release_metrics.get('total_bugfix_releases')
            total_hotfixes = release_metrics.get('total_hotfix_releases')
            current_release = int(total_releases) + 1
            current_features = int(total_features) + 1
            current_bugs = int(total_bugs) + 1
            current_hotfixes = int(total_hotfixes) + 1
                        
            yaml_content = f"""
            .total_releases = {current_release} |
            .total_feature_releases = {current_features} |
            .total_bugfix_releases = {current_bugs} |
            .total_hotfix_releases = {current_hotfixes} |
            .last_release.total_tickets = {total_deployments} |
            .last_release.features = {number_of_features} |
            .last_release.hotfixes = {number_of_hotfixes} |
            .last_release.bugs = {number_of_bugs} |
            .last_release.cfr = "{stringified_cfr}"
            """
            
            yq_operation = f"""yq -i '{yaml_content}' {target_data_file}"""
            os.system(yq_operation)
                
    else:
        print('Target file does not exist, creating one...')
        total_releases = 1    
        
        # create the yaml file
        with open(target_data_file, 'w') as fp:
            pass
        
        yaml_content = f"""
        .total_releases = {total_releases} |
        .total_feature_releases = {number_of_features} |
        .total_bugfix_releases = {number_of_bugs} |
        .total_hotfix_releases = {number_of_hotfixes} |
        .last_release.features = {number_of_features} |
        .last_release.date = "{current_date}" |
        .last_release.bugs = {number_of_bugs} |
        .last_release.hotfixes = {number_of_hotfixes}
        """
        
        yq_operation = f"""yq -i '{yaml_content}' {target_data_file}"""
        os.system(yq_operation)
        

# releases.yaml
def calculate_releases(target_data_file = 'metrics/releases.yaml'):
    if os.path.exists(target_data_file):
        print("Found existing target file, updating it with the latest release...")
                
        # Read the existing YAML content
        with open(target_data_file, "r") as yaml_file:
            release_dataset = yaml.safe_load(yaml_file)
            releases = release_dataset['releases']            
            current_release = len(releases) + 1
  
            
            index = current_release - 1
            yaml_content = f"""
            .releases["{index}"].no = {current_release} |
            .releases["{index}"].date = "{current_date}" |
            .releases["{index}"].features = {number_of_features} |
            .releases["{index}"].bugs = {number_of_bugs} |
            .releases["{index}"].hotfixes = {number_of_hotfixes} |
            .releases["{index}"].cfr = "{stringified_cfr}" 
            """      
                  
            print(yaml_content)        
            yq_operation = f"""yq -i '{yaml_content}' {target_data_file}"""
            os.system(yq_operation)
                
    else:
        print('Target file does not exist, creating one...')
        total_releases = 1    
        
        # create the yaml file
        with open(target_data_file, 'w') as fp:
            pass
        
        yaml_content = f"""
        .releases[0].no = {total_releases} |
        .releases[0].date = "{current_date}" |
        .releases[0].features = {number_of_features} |
        .releases[0].bugs = {number_of_bugs} |
        .releases[0].hotfixes = {number_of_hotfixes} |
        .releases[0].cfr = "{stringified_cfr}" 
        """
        
        yq_operation = f"""yq -i '{yaml_content}' {target_data_file}"""
        os.system(yq_operation)
        

if __name__ == "__main__":
    current_date = get_current_date()
    target_data_file = 'metrics/data.yaml'
    target_release_file = 'metrics/release.yaml'
        
    feature_messages, bug_messages, hotfix_messages = identify_commits()
    number_of_features = len(feature_messages)
    number_of_bugs = len(bug_messages)
    number_of_hotfixes = len(hotfix_messages)
    total_deployments = number_of_bugs + number_of_hotfixes + number_of_features
    total_issues = number_of_bugs + number_of_hotfixes
    cfr = calculate_change_failure_rate(total_deployments, total_issues)
    stringified_cfr = f"""{cfr} %"""
    
    print('calculating metrics for current release ....')
    calculate_metrics(target_data_file)
    print('updating the current release in the previous release dataset ....')
    calculate_releases(target_release_file)