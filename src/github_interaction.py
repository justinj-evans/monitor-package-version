import sys
import sys
from github import Github
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='action.yml arguments')
    parser.add_argument('--token', type=str, help='GitHub token')
    parser.add_argument('--repo', type=str, help='Repository name')
    parser.add_argument('--pull_number', type=str, help='Pull request number')
    parser.add_argument('--commit_sha', type=str, help='Commit SHA')
    parser.add_argument('--existing_sha', type=str, help='Existing SHA')
    parser.add_argument('--upgrade', type=bool, help='Whether to upgrade')
    parser.add_argument('--downgrade', type=bool, help='Whether to downgrade')
    parser.add_argument('--new_package', type=bool, help='Whether it is a new package')
    parser.add_argument('--additional_text', type=str, help='Additional text')
    args = parser.parse_args()
    return args

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

def get_argument(args, arg_name):
    try:
        index = args.index(arg_name)
        return args[index + 1]
    except (ValueError, IndexError):
        return None
