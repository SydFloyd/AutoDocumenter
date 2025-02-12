import os
import re
import sys
from llm import LLM

def get_python_files(repo_path):
    """Recursively finds all Python files in a given repository, ignoring certain directories."""
    ignored_dirs = {".venv", "__pycache__", ".git", "env", "venv"}
    python_files = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_existing_docstring(content):
    """Extracts the existing docstring if present."""
    match = re.match(r'\s*(""".*?"""|\'\'\'.*?\'\'\')', content, re.DOTALL)
    if match:
        return match.group(0), content[len(match.group(0)):].lstrip()
    return None, content

def generate_docstring(file_path, model):
    """Uses the LLM model to generate a useful docstring for the given Python file."""
    with open(file_path, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    _, code_without_docstring = extract_existing_docstring(original_content)
    
    prompt = f"""
    Analyze the following Python code and generate a concise but informative module-level docstring that explains its purpose and main functions.
    1. provide only the text, do not put it in a code block or even inside triple quotes.
    2. Don't provide any 
    
    Code:
    {code_without_docstring}
    
    Generated docstring:
    """
    response = model.prompt(prompt)
    return response.strip()

def replace_docstring(file_path, docstring):
    """Replaces the existing docstring or adds a new one if none exists."""
    with open(file_path, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    existing_docstring, remaining_content = extract_existing_docstring(original_content)
    new_content = f'"""\n{docstring}\n"""\n\n' + remaining_content
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

def update_docustring(file_path, model):
    model = LLM()
    new_docstring = generate_docstring(file_path, model)
    replace_docstring(file_path, new_docstring)
    print(f"Updated docstring for {file_path}")

if __name__ == "__main__":
    for file in sys.argv[1:]:  # Accept multiple files as arguments
        print(f"Processing {file}...")
        update_docustring(file)