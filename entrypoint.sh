#!/bin/sh

echo "Raw input arguments: $@"
# Use `set --` to correctly split arguments passed as a single string
set -- $@

echo "Processed arguments: $@"

python /app/AutoDocstring.py "$@"

echo "Script execution completed."