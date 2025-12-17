"""Error handling utilities for ArchiMate MCP Server."""

import os
import re
from typing import List, Optional, Tuple


def _extract_plantuml_error_details(debug_log: list) -> tuple[int, str, str, int]:
    """Extract PlantUML error details from debug log.

    Args:
        debug_log: List of debug log entries

    Returns:
        Tuple of (return_code, stderr, command, error_line)
    """
    plantuml_return_code = None
    plantuml_stderr = None
    plantuml_command = None
    error_line = None

    for entry in debug_log:
        if 'details' not in entry:
            continue

        details = entry['details']
        plantuml_return_code = _extract_return_code(details, plantuml_return_code)
        plantuml_command = _extract_command(details, plantuml_command)
        plantuml_stderr, error_line = _extract_error_output(details, plantuml_stderr, error_line)

    return plantuml_return_code, plantuml_stderr, plantuml_command, error_line


def _extract_return_code(details: dict, current_code) -> int:
    """Extract PlantUML return code from details."""
    if 'png_return_code' in details:
        return details['png_return_code']
    return current_code


def _extract_command(details: dict, current_command) -> str:
    """Extract PlantUML command from details."""
    if 'command' in details and 'plantuml.jar' in details['command']:
        return details['command']
    return current_command


def _extract_error_output(details: dict, current_stderr: str, current_error_line: int) -> tuple[str, int]:
    """Extract error output and line number from details."""
    output = details.get('output', '')
    has_error_line = 'Error line' in output
    has_diagram_errors = 'Some diagram description contains errors' in output

    if output and (has_error_line or has_diagram_errors):
        stderr = details['output']
        error_line = _extract_error_line_number(details['output']) if 'Error line' in details['output'] else current_error_line
        return stderr, error_line

    return current_stderr, current_error_line


def _extract_error_line_number(output: str) -> int:
    """Extract error line number from PlantUML output."""
    line_match = re.search(r'Error line (\d+)', output)
    return int(line_match.group(1)) if line_match else None


def _add_error_context_and_debug_info(error_parts: list, plantuml_code: str, error_line: int, error_export_dir: str) -> None:
    """Add problematic line context and debug information to error message.

    Args:
        error_parts: List to append error information to
        plantuml_code: The PlantUML code that caused the error
        error_line: The line number where the error occurred
        error_export_dir: Directory containing debug files
    """
    if plantuml_code and error_line:
        _add_problematic_line_context(error_parts, plantuml_code, error_line)

    if error_export_dir:
        _add_debug_information(error_parts, error_export_dir, plantuml_code)


def _add_problematic_line_context(error_parts: list, plantuml_code: str, error_line: int) -> None:
    """Add context around the problematic PlantUML line."""
    lines = plantuml_code.split('\n')
    if 1 <= error_line <= len(lines):
        problematic_line = lines[error_line - 1].strip()
        error_parts.append(f"**Problematic Line {error_line}:** `{problematic_line}`")

        context_lines = _build_context_lines(lines, error_line, problematic_line)
        if context_lines:
            error_parts.append("**Context:**")
            error_parts.append("```")
            error_parts.extend(context_lines)
            error_parts.append("```")


def _build_context_lines(lines: list, error_line: int, problematic_line: str) -> list:
    """Build context lines showing code around the error."""
    context_lines = []

    # Add line before error
    if error_line > 1:
        context_lines.append(f"{error_line-1:2d}: {lines[error_line-2].strip()}")

    # Add error line with warning
    context_lines.append(f"{error_line:2d}: {problematic_line} ⚠️")

    # Add line after error
    if error_line < len(lines):
        context_lines.append(f"{error_line+1:2d}: {lines[error_line].strip()}")

    return context_lines


def _add_debug_information(error_parts: list, error_export_dir: str, plantuml_code: str) -> None:
    """Add debug log and file information to error message."""
    _add_generation_log(error_parts, error_export_dir)

    if plantuml_code:
        _add_debug_file_list(error_parts, error_export_dir)


def _add_generation_log(error_parts: list, error_export_dir: str) -> None:
    """Add generation log contents to error message."""
    try:
        log_file_path = os.path.join(error_export_dir, "generation.log")
        if os.path.exists(log_file_path):
            _add_log_file_contents(error_parts, log_file_path)
        else:
            _add_log_file_reference(error_parts, error_export_dir)
    except Exception as log_read_error:
        _add_log_error_info(error_parts, error_export_dir, log_read_error)


def _add_log_file_contents(error_parts: list, log_file_path: str) -> None:
    """Add actual log file contents."""
    with open(log_file_path, 'r', encoding='utf-8') as f:
        log_contents = f.read()
    error_parts.append("**🔍 Debug Log:**")
    error_parts.append("```")
    error_parts.append(log_contents)
    error_parts.append("```")


def _add_log_file_reference(error_parts: list, error_export_dir: str) -> None:
    """Add reference to log file location."""
    error_parts.append(f"**🔍 Debug Files:** {error_export_dir}")
    error_parts.append("- `generation.log` - Complete debug trace")


def _add_log_error_info(error_parts: list, error_export_dir: str, error: Exception) -> None:
    """Add information about log reading error."""
    error_parts.append(f"**🔍 Debug Files:** {error_export_dir} (log read error: {error})")
    error_parts.append("- `generation.log` - Complete debug trace")


def _add_debug_file_list(error_parts: list, error_export_dir: str) -> None:
    """Add list of available debug files."""
    error_parts.append("**📄 Debug Files Available:**")
    error_parts.append(f"- `{error_export_dir}/diagram.puml` - Generated PlantUML code")
    error_parts.append(f"- `{error_export_dir}/input.json` - Original input data")


def _add_troubleshooting_suggestions(error_parts: list, plantuml_code: str, error_line: int, plantuml_command: str) -> None:
    """Add troubleshooting suggestions to error message.

    Args:
        error_parts: List to append troubleshooting information to
        plantuml_code: The PlantUML code that caused the error
        error_line: The line number where the error occurred
        plantuml_command: The PlantUML command that was executed
    """
    error_parts.append("**🛠️ Troubleshooting:**")

    if error_line and plantuml_code:
        _add_line_specific_suggestions(error_parts, plantuml_code, error_line)

    if plantuml_command:
        _add_command_testing_suggestion(error_parts, plantuml_command)


def _add_line_specific_suggestions(error_parts: list, plantuml_code: str, error_line: int) -> None:
    """Add suggestions based on the specific problematic line."""
    lines = plantuml_code.split('\n')
    if 1 <= error_line <= len(lines):
        problematic_line = lines[error_line - 1].strip()
        suggestions = _analyze_problematic_line(problematic_line)

        if suggestions:
            error_parts.extend(suggestions)
        else:
            error_parts.extend([
                "- Check PlantUML syntax on the problematic line",
                "- Verify element types and relationship syntax"
            ])


def _analyze_problematic_line(problematic_line: str) -> list:
    """Analyze the problematic line and return specific suggestions."""
    suggestions = []

    if "Application_Application_" in problematic_line:
        suggestions.append("- **Duplicate layer prefix detected** - This is a known issue being fixed")
    elif "_" not in problematic_line and "(" in problematic_line:
        suggestions.append("- **Missing element type prefix** - Check element type normalization")

    return suggestions


def _add_command_testing_suggestion(error_parts: list, plantuml_command: str) -> None:
    """Add suggestion to test PlantUML command directly."""
    error_parts.append(f"- **Test PlantUML directly:** `{plantuml_command.replace('/tmp/tmp', 'path/to/diagram')}`")


def _build_enhanced_error_response(original_error: Exception, debug_log: list, error_export_dir, plantuml_code: str = None) -> str:
    """Build comprehensive error response with debugging information for MCP tool.

    Args:
        original_error: The original exception that occurred
        debug_log: Debug log entries
        error_export_dir: Directory containing debug files
        plantuml_code: The PlantUML code that was generated (optional)

    Returns:
        Formatted error message string
    """
    try:
        # Extract PlantUML error details
        plantuml_return_code, plantuml_stderr, plantuml_command, error_line = _extract_plantuml_error_details(debug_log)

        # Build enhanced error message
        error_parts = []
        error_parts.append("❌ **PNG Generation Failed**")

        if plantuml_return_code:
            error_parts.append(f"**PlantUML Return Code:** {plantuml_return_code}")

        # Add original error message
        if original_error:
            error_parts.append(f"**Error:** {str(original_error)}")

        # Add PlantUML stderr if available
        if plantuml_stderr:
            error_parts.append("**PlantUML Output:**")
            error_parts.append("```")
            error_parts.append(plantuml_stderr)
            error_parts.append("```")

        # Add error context and debug info
        _add_error_context_and_debug_info(error_parts, plantuml_code, error_line, error_export_dir)

        # Add troubleshooting suggestions
        _add_troubleshooting_suggestions(error_parts, plantuml_code, error_line, plantuml_command)

        return "\n\n".join(error_parts)

    except Exception as build_error:
        # Fallback error message if error processing fails
        return f"❌ **Error Processing Failed**\n\nOriginal error: {str(original_error)}\n\nError processing failed: {str(build_error)}"