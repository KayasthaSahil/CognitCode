"""
Issue Data Modeler

This module provides functionality to format code analysis results into structured
JSON format suitable for consumption by LLM services. It converts CodeIssue objects
into a standardized JSON representation.

Author: CognitCode
"""

import json
from dataclasses import asdict
from typing import List

from src.analyzer import CodeIssue


def format_issues_to_json(issues: List[CodeIssue]) -> str:
    """
    Convert a list of CodeIssue objects into a JSON formatted string.
    
    This function takes a list of CodeIssue dataclass instances, converts each
    to a dictionary using dataclasses.asdict(), and then serializes the entire
    list into a JSON string suitable for API requests or LLM consumption.
    
    Args:
        issues (List[CodeIssue]): A list of CodeIssue objects to be formatted
        
    Returns:
        str: A JSON formatted string containing the serialized issues
        
    Example:
        >>> from src.analyzer import CodeIssue
        >>> from src.formatter import format_issues_to_json
        >>> 
        >>> issues = [
        ...     CodeIssue(line_number=5, issue_code="FUNC_TOO_LONG", 
        ...              description="Function has too many statements"),
        ...     CodeIssue(line_number=10, issue_code="MAGIC_NUMBER", 
        ...              description="Magic number detected")
        ... ]
        >>> json_output = format_issues_to_json(issues)
        >>> print(json_output)
        [{"line_number": 5, "issue_code": "FUNC_TOO_LONG", "description": "Function has too many statements"}, ...]
    """
    # Convert each CodeIssue object to a dictionary using dataclasses.asdict
    issues_dict = [asdict(issue) for issue in issues]
    
    # Serialize the list of dictionaries to JSON string
    json_string = json.dumps(issues_dict, indent=2)
    
    return json_string
