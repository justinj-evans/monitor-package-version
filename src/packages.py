import subprocess
import pkg_resources
from packaging import version

def get_current_version(package_name):
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None

def upgrade_package(package_name):
    print(f'upgrade_package')
    current_version = get_current_version(package_name)
    if current_version:
        print(f"Current version of {package_name}: {current_version}")
        subprocess.run(["pip", "install", "--upgrade", f"{package_name}=={pkg_resources.get_distribution(package_name).version}"])

def downgrade_package(package_name):
    print('downgrade_package')
    current_version = get_current_version(package_name)
    if current_version:
        print(f"Current version of {package_name}: {current_version}")
        previous_version = pkg_resources.get_distribution(package_name).version.split('.')
        print(previous_version)

        # example: 65.5.1 -> 65.5.0
        if int(previous_version[-1]) >= 1:
            previous_version[-1] = str(int(previous_version[-1])-1)
            previous_version = '.'.join(previous_version)
            subprocess.run(["pip", "install", f"{package_name}=={previous_version}"])

        # example: 65.5.0 -> 65.4.0 (testing only)
        if int(previous_version[-1]) == 0:
            previous_version[-2] = str(int(previous_version[-2])-1)
            previous_version = '.'.join(previous_version)
            subprocess.run(["pip", "install", f"{package_name}=={previous_version}"])


def compare_versions(old_version, new_version):
    if version.parse(new_version) > version.parse(old_version):
        return "Upgraded"
    elif version.parse(new_version) < version.parse(old_version):
        return "Downgraded"
    else:
        return "No-change"

# testing usage
if __name__ == "__main__":
    # package_name = "setuptools"
    # upgrade_package(package_name)
    # downgrade_package(package_name)

    result = compare_versions(old_version='1.26.3',new_version='1.26.2')
    print(result)