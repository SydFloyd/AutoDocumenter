#!/bin/sh
echo "Current directory: $(pwd)"

if [ ! -f "/app/entrypoint.sh" ]; then
    echo "Error: entrypoint.sh is missing!"
    exit 1
fi

echo "Running script with arguments: $@"
python /app/AutoDocstring.py "$@"
echo "Script execution completed."