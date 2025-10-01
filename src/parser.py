"""
AST Generation Service

This module provides functionality to parse Python code strings into Abstract Syntax Trees (AST)
using Python's built-in ast library. It handles syntax errors gracefully and returns
structured results.

Author: CognitCode
"""

import ast
from typing import Tuple, Union


def generate_ast_from_code(code_string: str) -> Tuple[ast.AST | None, str | None]:
    """
    Parse a Python code string into an Abstract Syntax Tree (AST).
    
    This function takes a raw Python code string as input and attempts to parse it
    into an AST object using Python's built-in ast.parse() function. It handles
    syntax errors gracefully by catching SyntaxError exceptions and returning
    user-friendly error messages.
    
    Args:
        code_string (str): The raw Python code string to be parsed.
        
    Returns:
        Tuple[ast.AST | None, str | None]: A tuple containing either:
            - (ast_object, None) on successful parsing
            - (None, error_message) on syntax error
            
    Example:
        >>> code = "def hello():\n    print('world')"
        >>> ast_tree, error = generate_ast_from_code(code)
        >>> if error is None:
        ...     print("Parsing successful!")
        ... else:
        ...     print(f"Error: {error}")
    """
    try:
        # Attempt to parse the code string into an AST
        parsed_ast = ast.parse(code_string)
        return (parsed_ast, None)
        
    except SyntaxError as e:
        # Handle syntax errors gracefully
        error_message = f"Error: Invalid Python syntax at line {e.lineno}"
        return (None, error_message)
