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
Analyze the following Python code and generate a module-level docstring.
1. Provide only the text, do not put it in a code block or inside triple quotes. Your response will be placed in the standard triple quotes automatically.
2. Adhere to PEP 257 and best practices for clarity and maintainability.

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