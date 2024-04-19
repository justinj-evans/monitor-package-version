import sys
from github import Github
import requests
import base64

def download_requirements_to_json(repo:str, commit:str, path:str):
    """Connect to Github Repository to extract file

    Args:
        repo (str): repository name
        commit (str): commit number
        path (str): path to requirements.txt

    Returns:
        requirements (dict): requirements.txt split into package (key) and version (value) format
    """
    base_url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={commit}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        data = response.json()
        content = data.get('content', '')
        
        # Decode base64 content
        decoded_content = base64.b64decode(content).decode('utf-8')

        # Split requirements by lines and convert to JSON format
        requirements_list = decoded_content.split('\n')

        requirements = {}
        for line in requirements_list:
            if '==' in line:
                package, version = line.strip("\ufeff").strip("\r").split("==")
                requirements[package] = version
        print(f'SHA: {commit} - Requirements: {requirements}')
        return requirements

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

def add_text_to_merge_request(token, owner, repo_name, pull_number, additional_text):
    github = Github(token)
    repo = github.get_repo(f"{repo_name}")
    pull_request = repo.get_pull(pull_number)
    new_description = f"{pull_request.body}\n\n## Additional Information\n\n{additional_text}"
    pull_request.edit(body=new_description)

def add_text_to_commit(token, repo_name, commit_sha, additional_text):
    github = Github(token)
    repo = github.get_repo(f"{repo_name}")
    commit = repo.get_commit(commit_sha)
    commit.create_comment(additional_text)

