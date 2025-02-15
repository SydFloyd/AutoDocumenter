"""
Module for generating and updating Python module-level docstrings using a language model.

This module provides functionality to extract existing docstrings, generate new ones using an LLM model, and replace or add docstrings in Python files. It is designed to automate the documentation process and ensure adherence to PEP 257 standards.

Functions:
    - extract_existing_docstring(content: str) -> Tuple[Optional[str], str]: Extracts existing docstrings from the content.
    - generate_docstring(file_path: str, model: LLM) -> str: Generates a module-level docstring using the LLM model.
    - replace_docstring(file_path: str, docstring: str): Replaces or adds a docstring in the specified file.
    - update_docustring(file_path: str, model: LLM): Updates the docstring of a file using the LLM model.

Classes:
    - LLM: A placeholder class for the language model used to generate docstrings.
"""

MAX_RETRY_DEPTH = 3
MAX_REFINEMENT_DEPTH = 3
GOOD_DOCSTRING_PRACTICE = """
A module docstring should:

Summarize the module’s purpose in a single sentence.
Optionally include additional paragraphs with details.
Optionally list key classes, functions, or exceptions if the module is large.
Example:

```
Utilities for handling text processing.

This module provides functions for text normalization, tokenization, and stopword removal.
It is designed for use in NLP pipelines.

Functions:
    - normalize_text(text: str) -> str: Lowercases and removes punctuation.
    - tokenize(text: str) -> List[str]: Splits text into words.
    - remove_stopwords(words: List[str]) -> List[str]: Removes common stopwords.

Exceptions:
    - TextProcessingError: Raised when an invalid input is encountered.
```
"""

import re
import sys
from llm import LLM

def extract_existing_docstring(content):
    """Extracts the existing docstring if present."""
    match = re.match(r'\s*(""".*?"""|\'\'\'.*?\'\'\')', content, re.DOTALL)
    if match:
        return match.group(0), content[len(match.group(0)):].lstrip()
    return None, content

def verify_docstring(file_path, model, refinement_depth, depth=MAX_RETRY_DEPTH):
    """Checks if the docstring needs updated. Returns True if needs updated, else False."""
    if depth == 0:
        return True

    with open(file_path, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    original_docstring, code_without_docstring = extract_existing_docstring(original_content)

    if refinement_depth == 0:
        guidance = """
The docstring can require an update for two reasons:
1. The code was updated and docstring is out-dated, or
2. The docstring doesn't follow PEP 257 or it deviates from best practices for clarity and maintainability.
"""
    else:
        guidance = """
The docstring requires an update only if it doesn't follow PEP 257 or it deviates from best practices for clarity and maintainability.
"""
    print("GUIDANCE:", guidance)
    prompt = f"""
You are an expert developer who specializes in good documentation. 
Your current task is to determine if the module docstring needs to be updated.
{guidance}

{GOOD_DOCSTRING_PRACTICE}

Docstring:
{original_docstring}

Code:
{code_without_docstring}

Respond 'True' if the docstring needs to be updated, otherwise 'False', followed by the reason the docstring needs updated.
"""
    response = model.prompt(prompt).strip()
    if response.startswith('True'):
        print(f"\n\nDocstring needs update.  Reasoning: {response}")
        return True, response[5:]
    elif response.startswith('False'):
        print(f"\n\nDocstring update not required.  Reasoning: {response}")
        return False, None
    else:
        print(f"Verifying docstring failed, retring (depth={depth})")
        verify_docstring(file_path, model, refinement_depth, depth-1)

def generate_docstring(file_path, reason, model):
    """Generates a useful docstring for the given Python file."""
    with open(file_path, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    old_docstring, code_without_docstring = extract_existing_docstring(original_content)
    
    prompt = f"""
Analyze the following Python code and generate a module-level docstring.
1. Provide only the text, do not put it in a code block or inside triple quotes. Your response will be placed in the standard triple quotes automatically.
2. Adhere to PEP 257 and best practices for clarity and maintainability.

{GOOD_DOCSTRING_PRACTICE}

Old Docstring:
{old_docstring}

Problems with Old Docstring:
{reason}

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
    new_content = f'"""\n{docstring}\n"""\n\n' + remaining_content + "\n"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

def update_docstring(file_path, model, refinement_depth):
    update_needed, reason = verify_docstring(file_path, model, refinement_depth)
    if update_needed:
        new_docstring = generate_docstring(file_path, reason, model)
        replace_docstring(file_path, new_docstring)
        return True
    return False

def auto_docstring(file_path, model, depth=MAX_REFINEMENT_DEPTH):
    for d in range(depth):
        updated = update_docstring(file_path, model, d)
        if not updated:
            print("Full docstring refinement depth acheived.")
            break
    print(f"Docstring refined for {file_path}.")

if __name__ == "__main__":
    print("AutoDocstring.py called with args:", sys.argv)
    try:
        if not sys.argv[1:]:
            print("No files provided! Exiting.")
            sys.exit(1)
        
        m = LLM()
        for file in sys.argv[1:]:  # Accept multiple files as arguments
            print("AutoDoctstring.py is looking at", file)
            file = file.strip()
            if file.endswith(".py"):
                print(f"Processing {file}...")
                auto_docstring(file, m)
            else:
                print("File didn't ent with '.py', skipping...")
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)
