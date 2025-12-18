# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:30
# Last Updated: 2025-12-18T11:40:30
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Export management utilities for ArchiMate MCP Server."""

import os
from datetime import datetime
from pathlib import Path


def get_exports_directory() -> Path:
    """Get the exports directory path, creating it if needed.

    Returns:
        Path to the exports directory in Documents folder
    """
    # Use Documents folder instead of project directory
    exports_dir = Path.home() / "Documents" / "archi-mcp-exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    return exports_dir


def create_export_directory() -> Path:
    """Create a timestamped directory for diagram exports.

    Returns:
        Path to the newly created export directory
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = get_exports_directory() / timestamp
    export_dir.mkdir(parents=True, exist_ok=True)
    return export_dir


def cleanup_failed_exports() -> None:
    """Move failed export attempts to failed_attempts subdirectory after successful PNG generation."""
    exports_dir = get_exports_directory()
    failed_attempts_dir = exports_dir / "failed_attempts"

    export_subdirs = _get_export_subdirectories(exports_dir)
    failed_dirs = _identify_failed_exports(export_subdirs)

    if failed_dirs:
        _move_failed_exports(failed_dirs, failed_attempts_dir)


def _get_export_subdirectories(exports_dir: Path) -> list:
    """Get all export subdirectories excluding failed_attempts."""
    return [d for d in exports_dir.iterdir() if d.is_dir() and d.name != "failed_attempts"]


def _identify_failed_exports(export_subdirs: list) -> list:
    """Identify export directories that don't contain any PNG file."""
    failed_dirs = []
    for export_dir in export_subdirs:
        # Check if directory contains any PNG files
        has_png = any(f.suffix.lower() == '.png' for f in export_dir.iterdir() if f.is_file())
        if not has_png:
            failed_dirs.append(export_dir)
    return failed_dirs


def _move_failed_exports(failed_dirs: list, failed_attempts_dir: Path) -> None:
    """Move failed export directories to the failed_attempts subdirectory."""
    failed_attempts_dir.mkdir(exist_ok=True)

    for failed_dir in failed_dirs:
        destination = failed_attempts_dir / failed_dir.name
        try:
            failed_dir.rename(destination)
            print(f"Moved failed export: {failed_dir.name} -> failed_attempts/")
        except Exception as e:
            print(f"Warning: Could not move {failed_dir.name}: {e}")