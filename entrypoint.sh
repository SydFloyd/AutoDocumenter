#!/bin/sh

# Debugging
echo "Raw input arguments: $@"

# Convert newline-separated input into an array
IFS=$'\n' read -r -d '' -a FILE_ARRAY <<< "$(printf "%s" "$@")"

echo "Running script with arguments: ${FILE_ARRAY[@]}"
python /app/AutoDocstring.py "${FILE_ARRAY[@]}"
echo "Script execution completed."