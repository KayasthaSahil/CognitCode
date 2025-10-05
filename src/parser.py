"""
AST Generation Service

This module provides functionality to parse Python code strings into Abstract Syntax Trees (AST)
using Python's built-in ast library. It handles syntax errors gracefully and returns
structured results.
"""

import ast
from typing import Tuple, Union


def generate_ast_from_code(code_string: str) -> Tuple[ast.AST | None, str | None]:
    """
    Parse a Python code string into an Abstract Syntax Tree (AST).
    """
    try:
        parsed_ast = ast.parse(code_string)
        return (parsed_ast, None)
        
    except SyntaxError as e:
        error_message = f"Error: Invalid Python syntax at line {e.lineno}"
        return (None, error_message)
