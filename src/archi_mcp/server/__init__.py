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

# Server functions are available through direct import from the server module
# These are imported at the end to avoid circular imports during module loading

def _import_server_functions():
    """Import server functions from the main server.py module."""
    try:
        import importlib.util
        import sys
        from pathlib import Path

        # Load the server.py file directly
        server_py_path = Path(__file__).parent.parent / 'server.py'
        spec = importlib.util.spec_from_file_location('server_impl', server_py_path)
        server_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(server_module)

        # Make functions available at module level
        globals().update({
            'translate_relationship_labels': server_module.translate_relationship_labels,
            'get_env_setting': server_module.get_env_setting,
            'is_config_locked': server_module.is_config_locked,
            'get_layout_setting': server_module.get_layout_setting,
            'detect_language_from_content': server_module.detect_language_from_content,
            'normalize_element_type': server_module.normalize_element_type,
            'normalize_layer': server_module.normalize_layer,
            'normalize_relationship_type': server_module.normalize_relationship_type,
            'validate_element_input': server_module.validate_element_input,
            'validate_relationship_input': server_module.validate_relationship_input,
            'validate_relationship_name': server_module.validate_relationship_name,
            '_validate_plantuml_renders': server_module._validate_plantuml_renders,
            '_create_archimate_diagram_impl': server_module._create_archimate_diagram_impl,
            '_load_diagram_from_file_impl': server_module._load_diagram_from_file_impl,
        })

        # Update __all__
        __all__.extend([
            'translate_relationship_labels',
            'get_env_setting',
            'is_config_locked',
            'get_layout_setting',
            'detect_language_from_content',
            'normalize_element_type',
            'normalize_layer',
            'normalize_relationship_type',
            'validate_element_input',
            'validate_relationship_input',
            'validate_relationship_name',
            '_validate_plantuml_renders',
            '_create_archimate_diagram_impl',
            '_load_diagram_from_file_impl',
        ])

    except Exception as e:
        # If import fails, functions won't be available
        pass

# Import functions after module is loaded
_import_server_functions()

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

# Import generator
from ..archimate import ArchiMateGenerator

# Create global generator instance
generator = ArchiMateGenerator()

# Import diagram creation function (lazy to avoid circular imports)
def create_archimate_diagram(diagram):
    """Lazy import wrapper for create_archimate_diagram."""
    from .request_processors.diagram_processor import create_archimate_diagram as _impl
    return _impl(diagram)

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
    "main"
]