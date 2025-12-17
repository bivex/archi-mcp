"""Debug utilities and error handling for the ArchiMate MCP server."""

import json
from pathlib import Path
from typing import List, Dict, Any

from .models import DiagramInput


def save_debug_log(export_dir: Path, log_entries: List[Dict[str, Any]]) -> Path:
    """Save debug log to export directory."""
    debug_log_path = export_dir / "debug_log.json"
    with open(debug_log_path, 'w', encoding='utf-8') as f:
        json.dump(log_entries, f, indent=2, ensure_ascii=False, default=str)
    return debug_log_path


def _save_failed_attempt(plantuml_code: str, diagram_input: DiagramInput, debug_log: list, error_message: str) -> None:
    """Save failed attempt data for debugging."""
    try:
        from .export_manager import create_export_directory
        export_dir = create_export_directory()
        debug_log_path = save_debug_log(export_dir, debug_log)

        # Save PlantUML code
        failed_puml_path = export_dir / "failed_diagram.puml"
        with open(failed_puml_path, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)

        # Save input data
        failed_input_path = export_dir / "failed_input.json"
        with open(failed_input_path, 'w', encoding='utf-8') as f:
            json.dump(diagram_input.model_dump(), f, indent=2, ensure_ascii=False)

        from ..utils.logging import get_logger
        logger = get_logger(__name__)
        logger.warning(f"Failed attempt saved to: {export_dir}")
        logger.warning(f"Error: {error_message}")

    except Exception as log_error:
        from ..utils.logging import get_logger
        logger = get_logger(__name__)
        logger.warning(f"Could not save debug log: {log_error}")