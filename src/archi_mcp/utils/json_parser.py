# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:24
# Last Updated: 2025-12-18T11:40:24
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""JSON parsing utilities with auto-fix capabilities."""

import json
import logging
import re
from typing import Any, Tuple

logger = logging.getLogger(__name__)


def parse_json_string(data: Any) -> Any:
    """Parse JSON string to dict for Claude Code compatibility with auto-fix.

    Claude Code sends parameters as JSON strings, while Claude Desktop sends objects.
    This function handles both cases automatically and attempts to fix common JSON errors.

    Args:
        data: Input data that might be a JSON string or already parsed dict

    Returns:
        Parsed dictionary/object
    """
    if isinstance(data, str):
        # Try standard JSON first
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            # Try JSON5 parser (handles single quotes, trailing commas, etc.)
            try:
                import json5
                result = json5.loads(data)
                logger.info("Auto-fixed JSON using json5 parser (handles single quotes, trailing commas, comments)")
                return result
            except Exception as json5_error:
                # JSON5 also failed, try manual auto-fix
                was_fixed, fixed_json, fix_description = _auto_fix_json(data)

                if was_fixed:
                    try:
                        # Try parsing the manually fixed JSON
                        result = json.loads(fixed_json)
                        logger.info(f"Auto-fixed JSON errors: {fix_description}")
                        return result
                    except json.JSONDecodeError as e2:
                        # Still failed after auto-fix, provide detailed error
                        error_details = _format_json_error(data, e2, was_fixed, fixed_json, fix_description)
                        raise ValueError(error_details) from e2
                else:
                    # No fixes applied, provide original error details
                    error_details = _format_json_error(data, e, False, data, "")
                    raise ValueError(error_details) from e

    # Not a string, return as-is
    return data


def _auto_fix_json(json_string: str) -> Tuple[bool, str, str]:
    """Automatically fix common JSON errors.

    Args:
        json_string: The potentially invalid JSON string

    Returns:
        Tuple of (was_fixed, fixed_json, fix_description)
    """
    original = json_string
    fixes_applied = []

    # Fix 0: CRITICAL - Replace single quotes with double quotes
    # This is the most common error when copying Python dict strings
    # Pattern: 'text' -> "text" (but preserve apostrophes in values)
    if "'" in json_string:
        json_string = json_string.replace("'", '"')
        fixes_applied.append("Replaced single quotes with double quotes")

    # Fix 1: Missing colons after property names
    # Pattern: "name" "value" -> "name": "value"
    pattern1 = r'("[\w_]+")(\s+)(")'
    if re.search(pattern1, json_string):
        json_string = re.sub(pattern1, r'\1:\3', json_string)
        fixes_applied.append("Added missing colons after property names")

    # Fix 2: Missing commas between properties (newline separated)
    # Pattern: "value"\n  "next": -> "value",\n  "next":
    pattern2 = r'("[^"]*"|\d+|true|false|null|\}|\])(\s*\n\s+)("[\w_]+":|{|"[\w_]+")'
    if re.search(pattern2, json_string):
        json_string = re.sub(pattern2, r'\1,\2\3', json_string)
        if "Added missing commas" not in fixes_applied:
            fixes_applied.append("Added missing commas between properties")

    # Fix 3: Missing commas in same line
    # Pattern: } { -> }, {
    pattern3 = r'(\}|\])(\s+)(\{|\[)'
    if re.search(pattern3, json_string):
        json_string = re.sub(pattern3, r'\1,\2\3', json_string)
        if "Added missing commas" not in fixes_applied:
            fixes_applied.append("Added missing commas between objects/arrays")

    # Fix 4: Property names without quotes
    # Pattern: {id: "value"} -> {"id": "value"}
    pattern4 = r'([{\s,])(\w+)(:)'
    if re.search(pattern4, json_string):
        json_string = re.sub(pattern4, r'\1"\2"\3', json_string)
        fixes_applied.append("Added quotes around property names")

    # Fix 5: Remove trailing commas
    # Pattern: "value",] or "value",} -> "value"]  or "value"}
    pattern5 = r',(\s*[}\]])'
    if re.search(pattern5, json_string):
        json_string = re.sub(pattern5, r'\1', json_string)
        fixes_applied.append("Removed trailing commas")

    # Fix 6: Extra opening braces
    # Pattern: {}\n  "id" -> {\n  "id"
    pattern6 = r'\{\}(\s*\n\s*")'
    if re.search(pattern6, json_string):
        json_string = re.sub(pattern6, r'{\1', json_string)
        fixes_applied.append("Removed extra braces")

    if fixes_applied:
        fix_desc = "; ".join(fixes_applied)
        return True, json_string, fix_desc

    return False, original, ""


def _format_json_error(
    original_json: str,
    error: json.JSONDecodeError,
    was_fixed: bool,
    fixed_json: str,
    fix_description: str
) -> str:
    """Format a detailed JSON parsing error message."""
    lines = original_json.split('\n')
    error_line = lines[error.lineno - 1] if error.lineno <= len(lines) else "N/A"
    error_col = error.colno if error.colno is not None else 0

    error_msg = "Invalid JSON string. JSON parsing failed: " + ".3f"

    if was_fixed:
        error_msg += f"\n\nAuto-fix attempted but still failed. Fixes applied: {fix_description}"
        error_msg += f"\nFixed JSON (still invalid):\n{fixed_json[:500]}{'...' if len(fixed_json) > 500 else ''}"

    # Provide helpful suggestions
    suggestions = []
    if "Expecting ',' delimiter" in str(error.msg):
        suggestions.append("Check for missing commas between properties")
    if "Expecting ':' delimiter" in str(error.msg):
        suggestions.append("Check for missing colons after property names")
    if "Unterminated string" in str(error.msg):
        suggestions.append("Check for unmatched quotes")
    if "'" in original_json:
        suggestions.append("Replace single quotes with double quotes")

    if suggestions:
        error_msg += "\n\nSuggestions:\n" + "\n".join(f"• {s}" for s in suggestions)

    return error_msg