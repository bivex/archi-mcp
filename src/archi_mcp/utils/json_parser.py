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

    # Identify and apply all fixes
    json_string, fixes_applied = _apply_json_fixes(json_string, fixes_applied)

    if fixes_applied:
        fix_desc = "; ".join(fixes_applied)
        return True, json_string, fix_desc

    return False, original, ""


def _apply_json_fixes(json_string: str, fixes_applied: list) -> Tuple[str, list]:
    """Apply all JSON fixing patterns to the string."""
    # Fix 0: CRITICAL - Replace single quotes with double quotes
    json_string, fixes_applied = _fix_single_quotes(json_string, fixes_applied)

    # Fix 1: Missing colons after property names
    json_string, fixes_applied = _fix_missing_colons(json_string, fixes_applied)

    # Fix 2: Missing commas between properties (newline separated)
    json_string, fixes_applied = _fix_missing_commas_newlines(json_string, fixes_applied)

    # Fix 3: Missing commas in same line
    json_string, fixes_applied = _fix_missing_commas_inline(json_string, fixes_applied)

    # Fix 4: Property names without quotes
    json_string, fixes_applied = _fix_unquoted_properties(json_string, fixes_applied)

    # Fix 5: Remove trailing commas
    json_string, fixes_applied = _fix_trailing_commas(json_string, fixes_applied)

    # Fix 6: Extra opening braces
    json_string, fixes_applied = _fix_extra_braces(json_string, fixes_applied)

    return json_string, fixes_applied


def _fix_single_quotes(json_string: str, fixes_applied: list) -> Tuple[str, list]:
    """Fix single quotes replaced with double quotes."""
    if "'" in json_string:
        json_string = json_string.replace("'", '"')
        fixes_applied.append("Replaced single quotes with double quotes")
    return json_string, fixes_applied


def _fix_missing_colons(json_string: str, fixes_applied: list) -> Tuple[str, list]:
    """Fix missing colons after property names."""
    pattern = r'("[\w_]+")(\s+)(")'
    if re.search(pattern, json_string):
        json_string = re.sub(pattern, r'\1:\3', json_string)
        fixes_applied.append("Added missing colons after property names")
    return json_string, fixes_applied


def _fix_missing_commas_newlines(json_string: str, fixes_applied: list) -> Tuple[str, list]:
    """Fix missing commas between properties (newline separated)."""
    pattern = r'("[^"]*"|\d+|true|false|null|\}|\])(\s*\n\s+)("[\w_]+":|{|"[\w_]+")'
    if re.search(pattern, json_string):
        json_string = re.sub(pattern, r'\1,\2\3', json_string)
        if "Added missing commas" not in fixes_applied:
            fixes_applied.append("Added missing commas between properties")
    return json_string, fixes_applied


def _fix_missing_commas_inline(json_string: str, fixes_applied: list) -> Tuple[str, list]:
    """Fix missing commas in same line."""
    pattern = r'(\}|\])(\s+)(\{|\[)'
    if re.search(pattern, json_string):
        json_string = re.sub(pattern, r'\1,\2\3', json_string)
        if "Added missing commas" not in fixes_applied:
            fixes_applied.append("Added missing commas between objects/arrays")
    return json_string, fixes_applied


def _fix_unquoted_properties(json_string: str, fixes_applied: list) -> Tuple[str, list]:
    """Fix property names without quotes."""
    pattern = r'([{\s,])(\w+)(:)'
    if re.search(pattern, json_string):
        json_string = re.sub(pattern, r'\1"\2"\3', json_string)
        fixes_applied.append("Added quotes around property names")
    return json_string, fixes_applied


def _fix_trailing_commas(json_string: str, fixes_applied: list) -> Tuple[str, list]:
    """Remove trailing commas."""
    pattern = r',(\s*[}\]])'
    if re.search(pattern, json_string):
        json_string = re.sub(pattern, r'\1', json_string)
        fixes_applied.append("Removed trailing commas")
    return json_string, fixes_applied


def _fix_extra_braces(json_string: str, fixes_applied: list) -> Tuple[str, list]:
    """Remove extra opening braces."""
    pattern = r'\{\}(\s*\n\s*")'
    if re.search(pattern, json_string):
        json_string = re.sub(pattern, r'{\1', json_string)
        fixes_applied.append("Removed extra braces")
    return json_string, fixes_applied


def _format_json_error(
    original_json: str,
    error: json.JSONDecodeError,
    was_fixed: bool,
    fixed_json: str,
    fix_description: str
) -> str:
    """Format a detailed JSON parsing error message."""
    error_details = _extract_error_details(original_json, error)
    error_msg = _build_error_message(error, error_details, was_fixed, fixed_json, fix_description)

    suggestions = _generate_error_suggestions(error.msg, original_json)
    if suggestions:
        error_msg += "\n\nSuggestions:\n" + "\n".join(f"• {s}" for s in suggestions)

    return error_msg


def _extract_error_details(original_json: str, error: json.JSONDecodeError) -> dict:
    """Extract error details from the JSON error."""
    lines = original_json.split('\n')
    return {
        'error_line': lines[error.lineno - 1] if error.lineno <= len(lines) else "N/A",
        'error_col': error.colno if error.colno is not None else 0
    }


def _build_error_message(error: json.JSONDecodeError, error_details: dict, was_fixed: bool, fixed_json: str, fix_description: str) -> str:
    """Build the main error message."""
    error_msg = "Invalid JSON string. JSON parsing failed: " + ".3f"

    if was_fixed:
        error_msg += f"\n\nAuto-fix attempted but still failed. Fixes applied: {fix_description}"
        error_msg += f"\nFixed JSON (still invalid):\n{fixed_json[:500]}{'...' if len(fixed_json) > 500 else ''}"

    return error_msg


def _generate_error_suggestions(error_msg: str, original_json: str) -> list:
    """Generate helpful suggestions based on the error."""
    suggestions = []
    error_str = str(error_msg)

    if "Expecting ',' delimiter" in error_str:
        suggestions.append("Check for missing commas between properties")
    if "Expecting ':' delimiter" in error_str:
        suggestions.append("Check for missing colons after property names")
    if "Unterminated string" in error_str:
        suggestions.append("Check for unmatched quotes")
    if "'" in original_json:
        suggestions.append("Replace single quotes with double quotes")

    return suggestions