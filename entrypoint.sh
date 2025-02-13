#!/bin/sh
echo "Current directory: $(pwd)"
echo "Listing files in workspace:"
ls -lah /github/workspace

echo "Running script..."
exec python /github/workspace/AutoDocstring.py "$@"
