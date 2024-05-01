#!/bin/sh -l

# Parameters
# - ${{ inputs.upgrade }}
# - ${{ inputs.downgrade }}
# - ${{ inputs.new_package }}
# - ${{ inputs.token }}
# - ${{ inputs.repository }}
# - ${{ inputs.existing_sha }}
# - ${{ inputs.commit_sha }}
# - ${{ inputs.pull_number }}
# - ${{ inputs.pull_number }}
# - ${{ inputs.pull_request_base_sha }}
# - ${{ inputs.pull_request_head_sha }}

# Print out the current directory
# echo "Contents of the current directory:"
# ls -l

# # Print out specific folders
# echo "Contents of the app directory:"
# ls -l /

# Run python main file
python /app/src/main.py \
    --upgrade "$1" \
    --downgrade "$2" \
    --new_package "$3"\
    --token "$4" \
    --repo "$5" \
    --existing_sha "$6" \
    --commit_sha "$7" \
    --pull_number "$8" \
    --pull_request_base_sha "$9" \
    --pull_request_head_sha "${10}" \

