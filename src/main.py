from github_interaction import add_text_to_commit, parse_args
from requirements import check_requirements, format_requirements_as_text, download_requirements_to_json

def user_notification():

    # get user input passed by args
    args = parse_args()

    # check if user input has been specified
    if args.new_package or args.upgrade or args.downgrade:

        user_input = {
            'new_packages': args.new_package,
            'upgraded_package': args.upgrade,
            'downgraded_package': args.downgrade
            }
    
        # extract requirements
        existing_requirements = download_requirements_to_json(repo=args.repo, commit=args.existing_sha, path="requirements.txt")
        new_requirements = download_requirements_to_json(repo=args.repo, commit=args.commit_sha, path="requirements.txt")

        # compare user's committed requirements from previous commit
        compare_requirements = check_requirements(existing_requirements=existing_requirements, new_requirements=new_requirements)

        # based on user input, adjust formatted text
        requirements_text = format_requirements_as_text(user_input=user_input, data=compare_requirements)

        # add formatted requirement check to commit message
        add_text_to_commit(token=args.token, repo_name=args.repo,
                        commit_sha=args.commit_sha, additional_text=requirements_text)

if __name__ == "__main__":

    user_notification()