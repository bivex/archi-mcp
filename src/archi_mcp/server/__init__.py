"""Server components for ArchiMate MCP."""

import socket

# Import main components
from .main import mcp

# Import models and utilities
from .models import ElementInput, RelationshipInput, DiagramInput
from .main import mcp

# Import server functions
from .http_server import (
    start_http_server,
    stop_http_server,
    http_server_port,
    http_server_thread,
    http_server_running,
    find_free_port
)

# Import main server functions - using lazy imports to avoid circular dependencies
def _get_server_module():
    """Lazy import of server module to avoid circular imports."""
    import importlib
    return importlib.import_module('archi_mcp.server')

# Wrapper functions for server functions
def translate_relationship_labels(*args, **kwargs):
    return _get_server_module().translate_relationship_labels(*args, **kwargs)

def get_env_setting(*args, **kwargs):
    return _get_server_module().get_env_setting(*args, **kwargs)

def is_config_locked(*args, **kwargs):
    return _get_server_module().is_config_locked(*args, **kwargs)

def get_layout_setting(*args, **kwargs):
    return _get_server_module().get_layout_setting(*args, **kwargs)

def detect_language_from_content(*args, **kwargs):
    return _get_server_module().detect_language_from_content(*args, **kwargs)

def normalize_element_type(*args, **kwargs):
    return _get_server_module().normalize_element_type(*args, **kwargs)

def normalize_layer(*args, **kwargs):
    return _get_server_module().normalize_layer(*args, **kwargs)

def normalize_relationship_type(*args, **kwargs):
    return _get_server_module().normalize_relationship_type(*args, **kwargs)

def validate_element_input(*args, **kwargs):
    return _get_server_module().validate_element_input(*args, **kwargs)

def validate_relationship_input(*args, **kwargs):
    return _get_server_module().validate_relationship_input(*args, **kwargs)

def validate_relationship_name(*args, **kwargs):
    return _get_server_module().validate_relationship_name(*args, **kwargs)

def _validate_plantuml_renders(*args, **kwargs):
    return _get_server_module()._validate_plantuml_renders(*args, **kwargs)

def _create_archimate_diagram_impl(*args, **kwargs):
    return _get_server_module()._create_archimate_diagram_impl(*args, **kwargs)

def _load_diagram_from_file_impl(*args, **kwargs):
    return _get_server_module()._load_diagram_from_file_impl(*args, **kwargs)

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
    "detect_language_from_content",
    "normalize_element_type",
    "normalize_layer",
    "normalize_relationship_type",
    "validate_element_input",
    "validate_relationship_input",
    "validate_relationship_name",
    "_validate_plantuml_renders",
    # "create_archimate_diagram",  # Temporarily disabled due to circular import
    "create_diagram_from_file",
    "test_element_normalization",
    "_create_archimate_diagram_impl",
    "_load_diagram_from_file_impl",
    "cleanup_failed_exports",
    "_add_markdown_header",
    "assert_plantuml_valid",
    "_extract_plantuml_error_details",
    "_add_error_context_and_debug_info",
    "_add_troubleshooting_suggestions",
    "_build_enhanced_error_response",
    "get_exports_directory",
    "create_export_directory",
    "main"
]