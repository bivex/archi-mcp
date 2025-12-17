"""Server components for ArchiMate MCP."""

import socket

# Import main components
from .main import mcp

# Import models and utilities
from .models import ElementInput, RelationshipInput, DiagramInput

# Import server functions
from .http_server import (
    start_http_server,
    stop_http_server,
    http_server_port,
    http_server_thread,
    http_server_running,
    find_free_port
)

# Import functions and constants from the refactored modules
from .config import get_env_setting, is_config_locked, get_layout_setting, get_layout_parameters_info
from .validators import (
    normalize_element_type, normalize_layer, normalize_relationship_type,
    validate_element_input, validate_relationship_input, validate_relationship_name,
    ELEMENT_TYPE_MAPPING, VALID_LAYERS, VALID_RELATIONSHIPS
)
from .language import translate_relationship_labels, detect_language_from_content
from .plantuml_validator import _validate_plantuml_renders, _validate_png_file
from .diagram_engine import _create_archimate_diagram_impl, _load_diagram_from_file_impl
from .markdown_generator import generate_architecture_markdown
from .debug_utils import save_debug_log

def _add_markdown_header(*args, **kwargs):
    return _get_server_module()._add_markdown_header(*args, **kwargs)

# Import export manager functions
from .export_manager import (
    get_exports_directory,
    create_export_directory,
    cleanup_failed_exports,
)

# Import error handler functions
from .error_handler import (
    _extract_plantuml_error_details,
    _add_error_context_and_debug_info,
    _add_troubleshooting_suggestions,
    _build_enhanced_error_response,
)

# Import generator and validator
from ..archimate import ArchiMateGenerator, ArchiMateValidator

# Create global generator and validator instances
generator = ArchiMateGenerator()
validator = ArchiMateValidator()

# Import diagram creation function directly (should be FunctionTool with .fn attribute)
from .request_processors.diagram_processor import create_archimate_diagram

# Utility functions
def assert_plantuml_valid(plantuml_code: str):
    """Assert that PlantUML code has basic valid structure."""
    assert "@startuml" in plantuml_code
    assert "@enduml" in plantuml_code
    assert "!include <archimate/Archimate>" in plantuml_code

# Import diagram processing functions
# from .request_processors.diagram_processor import create_archimate_diagram  # Temporarily disabled due to circular import

# Import utility functions (defined inline to avoid circular imports)
def find_free_port() -> int:
    """Find a free port for HTTP server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
        return port

__all__ = [
    "mcp",
    "ElementInput",
    "RelationshipInput",
    "DiagramInput",
    "find_free_port",
    "start_http_server",
    "stop_http_server",
    "http_server_port",
    "http_server_thread",
    "http_server_running",
    "translate_relationship_labels",
    "get_env_setting",
    "is_config_locked",
    "get_layout_setting",
    "get_layout_parameters_info",
    "detect_language_from_content",
    "normalize_element_type",
    "normalize_layer",
    "normalize_relationship_type",
    "validate_element_input",
    "validate_relationship_input",
    "validate_relationship_name",
    "_validate_plantuml_renders",
    "_validate_png_file",
    "_create_archimate_diagram_impl",
    "_load_diagram_from_file_impl",
    "generate_architecture_markdown",
    "save_debug_log",
    "ELEMENT_TYPE_MAPPING",
    "VALID_LAYERS",
    "VALID_RELATIONSHIPS",
    "cleanup_failed_exports",
    "_add_markdown_header",
    "assert_plantuml_valid",
    "_extract_plantuml_error_details",
    "_add_error_context_and_debug_info",
    "_add_troubleshooting_suggestions",
    "_build_enhanced_error_response",
    "get_exports_directory",
    "create_export_directory",
    "generator",
    "validator",
    "main"
]