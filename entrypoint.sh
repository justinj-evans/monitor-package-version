#!/bin/sh -l

# Parameters
# - ${{ inputs.upgrade }}
# - ${{ inputs.downgrade }}
# - ${{ inputs.new_package }}
# - ${{ inputs.token }}
# - ${{ github.repository }}
# - ${{ github.sha }}
# - ${{ github.event.before }}

# Print out the current directory
echo "Contents of the current directory:"
ls -l

# Print out specific folders
echo "Contents of the app directory:"
ls -l /

# Run python main file
python /app/src/main.py \
    --upgrade "$1" \
    --downgrade "$2" \
    --new_package "$3"\
    --token "$4" \
    --repo "$5" \
    --commit_sha "$6" \
    --existing_sha "$7" \

