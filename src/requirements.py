from packaging import version
import json

def compare_package_versions(old_version, new_version):
    if version.parse(new_version) > version.parse(old_version):
        return "Upgraded"
    elif version.parse(new_version) < version.parse(old_version):
        return "Downgraded"
    else:
        return "No-change"

def check_requirements(existing_requirements:dict, new_requirements:dict, ):
    """
    Args:
        new_requirements (dict): commited SHA requirements.txt in dict form
        existing_requirements (dict): existing SHA requirements.txt in dict form

    Returns:
        outputs (dict): categorized requirements.txt diff 
    """

    # Compare dictionaries to find new packages or updated versions
    new_packages = {pkg: version for pkg, version in new_requirements.items() if pkg not in existing_requirements}
    updated_packages = {pkg: version for pkg, version in new_requirements.items() if pkg in existing_requirements and existing_requirements[pkg] != version}

    upgraded_package = {}
    downgraded_package = {}

    # loop through updated packags to determine if upgraded, downgraded
    if updated_packages:
        for package, version in updated_packages.items():
            print(f"Updated Package: {package}: {existing_requirements[package]} -> {version}\n")
            version_value = compare_package_versions(existing_requirements[package],version)

            # add to exported dictionaries 
            if version_value == 'Upgraded':
                upgraded_package[package]=[existing_requirements[package],version]
            if version_value == 'Downgraded':
                downgraded_package[package]=[existing_requirements[package],version]

    outputs = {
        "new_packages": new_packages,
        "upgraded_packages": upgraded_package,
        "downgraded_packages": downgraded_package
    }

    return outputs

def format_requirements_as_text(data: json, user_input: json, ):
    """
    Args:
        data (json): categorized requirements diff 
        user_input (json): user decision on how to report on requirements diff

    Returns:
        output_text (str): formatted text to comment in Github.
    """

    outputs = []

    # Github Action text to users
    standard_text = "Automated message generated by Github Action 'Monitor Package Version' \n"
    outputs.append(standard_text)

    # Loop through each key and generate the text block if include flag is True
    for key in data:
        if user_input[key] and data.get(key):
            text = f"{key.capitalize().replace('_', ' ')}:\n"
            for package, version in data[key].items():
                if isinstance(version, list):
                    version_text = ' -> '.join(version)
                else:
                    version_text = version
                text += f"- {package}: {version_text}\n"
            
            outputs.append(text)

    # Join all text blocks into a single string
    output_text = '\n'.join(outputs)

    # only add output message if differences found
    if output_text == standard_text:
            return ""
    else:
        print(f'Formatted outputs:\n\n{output_text}')
        return output_text

if __name__ == "__main__":

    # synthetic versions
    # result = compare_versions(old_version='1.3.1',new_version='1.2.0')
    # print(result)

    # synthetic requirements
    existing_requirements = {'aiohttp': '3.9.3', 'aiosignal': '1.3.1', 'async-timeout': '4.0.3', 'setuptools': '69.1.0'}
    new_requirements = {'aiohttp': '3.9.3', 'aiosignal': '1.3.2', 'async-timeout': '4.0.2', 'setuptools': '69.1.0', 'pandas': '1.0.0'}
    user_input = {'new_packages': True,'upgraded_packages': True,'downgraded_packages': True}

    requirements_comparison = check_requirements(existing_requirements=existing_requirements,new_requirements=new_requirements)
    requirements_text = format_requirements_as_text(data=requirements_comparison,user_input=user_input)

