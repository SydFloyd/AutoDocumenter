#!/bin/sh
echo "Current directory: $(pwd)"
echo "Listing files in workspace:"
ls -lah /app

if [ ! -f "/app/entrypoint.sh" ]; then
    echo "Error: entrypoint.sh is missing!"
    exit 1
fi

echo "Running script..."
exec python /app/AutoDocstring.py "$@"
