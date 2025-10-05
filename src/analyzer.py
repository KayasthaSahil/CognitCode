"""
Analysis Rule Engine: Abstract Syntax Trees (AST)

"""

import ast
from dataclasses import dataclass
from typing import List


@dataclass
class CodeIssue:
    """
    Represents a single code smell found in the AST.
    """
    line_number: int
    issue_code: str
    description: str


class CodeSmellVisitor(ast.NodeVisitor):
    """
    AST visitor that detects various code smells by traversing the syntax tree.
    """
    
    def __init__(self):
        self.issues: List[CodeIssue] = []
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Visit a function definition node and check for code smells.
        """
        if len(node.body) > 20:
            issue = CodeIssue(
                line_number=node.lineno,
                issue_code="FUNC_TOO_LONG",
                description=f"Function '{node.name}' has {len(node.body)} statements, exceeding the threshold of 20."
            )
            self.issues.append(issue)
        
        self.generic_visit(node)
    
    def visit_Constant(self, node: ast.Constant) -> None:
        """
        Visit a constant node and check for magic numbers.
        """

        if isinstance(node.value, (int, float)):
            issue = CodeIssue(
                line_number=node.lineno,
                issue_code="MAGIC_NUMBER",
                description=f"The constant '{node.value}' is a magic number; consider defining it as a named constant."
            )
            self.issues.append(issue)
        
        self.generic_visit(node)


def run_analysis(ast_tree: ast.AST) -> List[CodeIssue]:
    """
    Run static analysis on an AST to detect code smells.
    """
    visitor = CodeSmellVisitor()
    
    visitor.visit(ast_tree)
    
    return visitor.issues
