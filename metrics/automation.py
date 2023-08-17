
import subprocess
import re
import os
import datetime
import yaml

def get_current_date():
    today = datetime.date.today()
    formatted_date = today.strftime("%d-%m-%Y")
    return formatted_date # '17-08-2023'

def calc_cfr(n_issues, n_deps):
    cfr = (n_issues / n_deps) * 100
    return round(cfr, 2) # 22.12

def calc_hotfix_to_release_ratio(n_releases, n_hotfxies):
    if n_releases <= 0:
        raise ValueError("Number of releases must be greater than 0")
    if n_hotfxies < 0:
        raise ValueError("Number of issues cannot be negative")
    cfr = calc_cfr(n_hotfxies , n_releases)
    return cfr 

def calc_failure_to_tickets_ratio(n_total_tickets, n_failures):
    if n_total_tickets <= 0:
        raise ValueError("Number of tickets must be greater than 0")
    if n_failures < 0:
        raise ValueError("Number of issues cannot be negative")
    cfr = calc_cfr(n_failures , n_total_tickets)
    return cfr 

def calc_feature_to_bug_ratio(n_features, n_bugs):
    # if n_features <= 0:
    #     raise ValueError("Number of tickets must be greater than 0")
    # TODO: discuss to add the above check ^
    
    if n_features < 0:
        raise ValueError("Number of issues cannot be negative")
    if n_bugs < 0:
        raise ValueError("Number of issues cannot be negative")
    cfr = calc_cfr(n_bugs , n_features)
    return cfr 

def calc_releases_without_bugs(n_releases, n_bugfree_releases):
    if n_bugfree_releases < 0:
        raise ValueError("Number of issues cannot be negative")
    if n_releases < 0:
        raise ValueError("Number of issues cannot be negative")
    cfr = calc_cfr(n_bugfree_releases , n_releases)
    return cfr     


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
            last_release = release_metrics.get('last_release')
            previous_n_tickets = last_release.get('total_tickets')
            
            current_release = int(total_releases) + 1
            current_features = int(total_features) + 1
            current_bugs = int(total_bugs) + 1
            current_hotfixes = int(total_hotfixes) + 1
            total_releases_without_hotfixes = current_release - total_hotfixes
            
            # calculate hotfixes per deployments ratio for this release 
            hotfix_to_release_ratio = calc_hotfix_to_release_ratio(total_deployments, number_of_hotfixes)
            
            # calculate failures for tickets from previous release ratio 
            failures_to_total_previous_tickets_ratio = calc_failure_to_tickets_ratio(previous_n_tickets, number_of_bugs)

            # calculate feature to bug ratio
            feature_to_bug_ratio = calc_feature_to_bug_ratio(number_of_features, number_of_bugs)

            # calculate release without bugs             
            current_total_hotfixes = current_hotfixes if (number_of_hotfixes == 0) else total_hotfixes
            release_without_bugs_ratio = calc_releases_without_bugs(current_release, current_total_hotfixes)
            
            yaml_content = f"""
            .total_releases = {current_release} |
            .total_feature_releases = {current_features} |
            .total_bugfix_releases = {current_bugs} |
            .total_hotfix_releases = {current_hotfixes} |
            .total_releases_without_hotfixes = {total_releases_without_hotfixes} |
            .last_release.total_tickets = {total_deployments} |
            .last_release.features = {number_of_features} |
            .last_release.hotfixes = {number_of_hotfixes} |
            .last_release.bugs = {number_of_bugs} |
            .last_release.hotfix_to_release_ratio = "{hotfix_to_release_ratio} %" |
            .last_release.failures_to_total_previous_tickets_ratio = "{failures_to_total_previous_tickets_ratio} %" |
            .last_release.feature_to_bug_ratio = "{feature_to_bug_ratio} %" |
            .last_release.release_without_bugs_ratio = "{release_without_bugs_ratio} %"
            """
            
            yq_operation = f"""yq -i '{yaml_content}' {target_data_file}"""
            os.system(yq_operation)
                
    else:
        print('Target file does not exist, creating one...')
        
        # create the yaml file
        with open(target_data_file, 'w') as fp:
            pass
        
        # assuming this will be the first release
        total_releases = 1    
        yaml_content = f"""
        .total_releases = {total_releases} |
        .total_feature_releases = {number_of_features} |
        .total_bugfix_releases = {number_of_bugs} |
        .total_hotfix_releases = {number_of_hotfixes} |
        .total_releases_without_hotfixes = {total_releases} |
        .last_release.features = {number_of_features} |
        .last_release.total_tickets = {number_of_features} |
        .last_release.date = "{current_date}" |
        .last_release.bugs = {number_of_bugs} |
        .last_release.hotfixes = {number_of_hotfixes} |
        .last_release.hotfix_to_release_ratio = "0 %" |
        .last_release.failures_to_total_previous_tickets_ratio = "0 %" |
        .last_release.feature_to_bug_ratio = "0 %" |
        .last_release.release_without_bugs_ratio = "0 %"
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
  
            # todo: add isHotfix: true/false logic
            index = current_release - 1
            yaml_content = f"""
            .releases["{index}"].no = {current_release} |
            .releases["{index}"].date = "{current_date}" |
            .releases["{index}"].features = {number_of_features} |
            .releases["{index}"].bugs = {number_of_bugs} |
            .releases["{index}"].hotfixes = {number_of_hotfixes}
            """      
                  
            yq_operation = f"""yq -i '{yaml_content}' {target_data_file}"""
            os.system(yq_operation)
                
    else:
        print('Target file does not exist, creating one...')
        
        # create the yaml file
        with open(target_data_file, 'w') as fp:
            pass

        # assuming this will be the first release    
        total_releases = 1    
        yaml_content = f"""
        .releases[0].no = {total_releases} |
        .releases[0].date = "{current_date}" |
        .releases[0].features = {number_of_features} |
        .releases[0].bugs = {number_of_bugs} |
        .releases[0].hotfixes = {number_of_hotfixes}
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
    
    print('calculating metrics for current release ....')
    calculate_metrics(target_data_file)
    print('updating the current release in the previous release dataset ....')
    calculate_releases(target_release_file)