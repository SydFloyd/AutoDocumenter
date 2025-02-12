import re
import sys
from llm import LLM

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
1. Provide only the text, do not put it in a code block or inside triple quotes, I'll do this for you.
2. Adhere to PEP 257 and best practices for clarity and maintainability.

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
    new_docstring = generate_docstring(file_path, model)
    replace_docstring(file_path, new_docstring)
    print(f"Updated docstring for {file_path}")

if __name__ == "__main__":
    m = LLM()
    for file in sys.argv[1:]:  # Accept multiple files as arguments
        print(f"Processing {file}...")
        update_docustring(file, m)