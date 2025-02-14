#!/bin/sh
echo "Current directory: $(pwd)"

if [ ! -f "/app/entrypoint.sh" ]; then
    echo "Error: entrypoint.sh is missing!"
    exit 1
fi

echo "Python version:"
python --version || echo "Python is missing!"

echo "Running script with arguments: $@"
# python /app/AutoDocstring.py "$@"
PYTHONUNBUFFERED=1 python /app/AutoDocstring.py "$@" | tee /dev/tty
echo "Script execution completed."