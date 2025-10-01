"""
Analysis Rule Engine

This module provides functionality to analyze Abstract Syntax Trees (AST) and detect
various "code smells" or quality issues in Python code. It uses the visitor pattern
to traverse AST nodes and apply specific analysis rules.

Author: CognitCode
"""

import ast
from dataclasses import dataclass
from typing import List


@dataclass
class CodeIssue:
    """
    Represents a single code smell found in the AST.
    
    Attributes:
        line_number (int): The line number where the issue was detected
        issue_code (str): A unique identifier for the type of issue (e.g., "FUNC_TOO_LONG", "MAGIC_NUMBER")
        description (str): A human-readable description of the issue
    """
    line_number: int
    issue_code: str
    description: str


class CodeSmellVisitor(ast.NodeVisitor):
    """
    AST visitor that detects various code smells by traversing the syntax tree.
    
    This class inherits from ast.NodeVisitor and implements specific visit methods
    to analyze different types of AST nodes for potential code quality issues.
    """
    
    def __init__(self):
        """Initialize the visitor with an empty list to store detected issues."""
        self.issues: List[CodeIssue] = []
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Visit a function definition node and check for code smells.
        
        This method checks if a function has too many statements (nodes) in its body,
        which could indicate that the function is doing too much and should be refactored.
        
        Args:
            node (ast.FunctionDef): The function definition node to analyze
        """
        # Check if function has more than 20 nodes in its body
        if len(node.body) > 20:
            issue = CodeIssue(
                line_number=node.lineno,
                issue_code="FUNC_TOO_LONG",
                description=f"Function '{node.name}' has {len(node.body)} statements, exceeding the threshold of 20."
            )
            self.issues.append(issue)
        
        # Continue visiting child nodes
        self.generic_visit(node)
    
    def visit_Constant(self, node: ast.Constant) -> None:
        """
        Visit a constant node and check for magic numbers.
        
        This method identifies numeric constants (integers and floats) that might
        be "magic numbers" - hardcoded values that should be replaced with named constants.
        
        Args:
            node (ast.Constant): The constant node to analyze
        """
        # Check if the constant is a numeric value (int or float)
        if isinstance(node.value, (int, float)):
            issue = CodeIssue(
                line_number=node.lineno,
                issue_code="MAGIC_NUMBER",
                description=f"The constant '{node.value}' is a magic number; consider defining it as a named constant."
            )
            self.issues.append(issue)
        
        # Continue visiting child nodes
        self.generic_visit(node)


def run_analysis(ast_tree: ast.AST) -> List[CodeIssue]:
    """
    Run static analysis on an AST to detect code smells.
    
    This function serves as the public interface for the analysis engine.
    It creates a visitor instance, traverses the AST, and returns all detected issues.
    
    Args:
        ast_tree (ast.AST): The Abstract Syntax Tree to analyze
        
    Returns:
        List[CodeIssue]: A list of all detected code issues, empty if none found
        
    Example:
        >>> import ast
        >>> from src.analyzer import run_analysis
        >>> 
        >>> code = '''
        ... def long_function():
        ...     x = 1
        ...     y = 2
        ...     # ... many more statements
        ... '''
        >>> tree = ast.parse(code)
        >>> issues = run_analysis(tree)
        >>> for issue in issues:
        ...     print(f"Line {issue.line_number}: {issue.description}")
    """
    # Create a visitor instance
    visitor = CodeSmellVisitor()
    
    # Visit the AST to detect issues
    visitor.visit(ast_tree)
    
    # Return the collected issues
    return visitor.issues
