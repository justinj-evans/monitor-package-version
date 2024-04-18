import pkg_resources
from packages import compare_versions
import json
import requests
import base64

def download_requirements_to_json(repo:str, commit:str, path:str):
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

def check_requirements(new_requirements:dict, existing_requirements:dict):

    # Compare dictionaries to find new packages or updated versions
    new_packages = {pkg: version for pkg, version in new_requirements.items() if pkg not in existing_requirements}
    updated_packages = {pkg: version for pkg, version in new_requirements.items() if pkg in existing_requirements and existing_requirements[pkg] != version}

    # Print new packages or updated versions
    # if new_packages:
    #     for package, version in new_packages.items():
    #         print(f"New Package: {package}=={version}\n")

    upgraded_package = {}
    downgraded_package = {}

    # loop through updated packags to determine if upgraded, downgraded
    if updated_packages:
        for package, version in updated_packages.items():
            print(f"Updated Package: {package}: {existing_requirements[package]} -> {version}\n")

            version_value = compare_versions(existing_requirements[package],version)

            # add to exported dictionaries 
            if version_value == 'Upgraded':
                upgraded_package[package]=[existing_requirements[package],version]
            if version_value == 'Downgraded':
                downgraded_package[package]=[existing_requirements[package],version]


    outputs = {
        "new_packages": new_packages,
        "upgraded_package": updated_packages,
        "downgraded_package": downgraded_package
    }
    #print(f'Outputs: {outputs}')
    return outputs


def format_requirements_as_text(user_input: json, data: json):
    """
    Expected format:

    outputs = {
        "new_packages": new_packages,
        "upgraded_package": updated_packages,
        "downgraded_package": downgraded_package
    }

    user_input = {
    'new_packages': True,
    'upgraded_package': False,
    'downgraded_package': True
    }
    """

    outputs = []

    # Loop through each key and generate the text block if include flag is True
    for key in data:
        if user_input.get(key, False):
            text = f"{key.capitalize().replace('_', ' ')}:\n"
            for package, version in data[key].items():
                if isinstance(version, list):
                    version_text = ', '.join(version)
                else:
                    version_text = version
                text += f"- {package}: {version_text}\n"
            outputs.append(text)

    # Join all text blocks into a single string
    output_text = '\n'.join(outputs)
    print(f'Formatted outputs: \n {output_text}')
    return output_text

# testing usage
if __name__ == "__main__":

    existing_requirements = {'aiohttp': '3.9.3', 'aiosignal': '1.3.1', 'async-timeout': '4.0.3', 'setuptools': '69.1.0'}

    requirements_comparison = check_requirements(existing_requirements)
    user_input = {
    'new_packages': True,
    'upgraded_package': False,
    'downgraded_package': True
    }
    format_requirements_as_text(user_input,requirements_comparison)
