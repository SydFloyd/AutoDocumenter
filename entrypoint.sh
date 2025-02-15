#!/bin/sh
# Debugging: Show raw input arguments
echo "Raw input arguments: $@"

# Use `set --` to correctly split arguments passed as a single string
set -- $@

# Debugging: Show processed arguments
echo "Processed arguments: $@"

# Pass arguments correctly to Python script
python /app/AutoDocstring.py "$@"

echo "Script execution completed."