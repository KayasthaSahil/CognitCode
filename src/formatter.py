"""
Issue Data Modeler

This module provides functionality to format code analysis results into structured
JSON format suitable for consumption by LLM services. It converts CodeIssue objects
into a standardized JSON representation.
"""

import json
from dataclasses import asdict
from typing import List

from src.analyzer import CodeIssue


def format_issues_to_json(issues: List[CodeIssue]) -> str:
    """
    Convert a list of CodeIssue objects into a JSON formatted string.
    Returns:
        str: A JSON formatted string containing the serialized issues
    """

    issues_dict = [asdict(issue) for issue in issues]

    json_string = json.dumps(issues_dict, indent=2)
    
    return json_string
