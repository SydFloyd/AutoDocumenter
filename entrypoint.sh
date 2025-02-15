#!/bin/sh
echo "Running script with arguments: $@"
python /app/AutoDocstring.py "$@"
echo "Script execution completed."