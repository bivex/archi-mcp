"""Server components for ArchiMate MCP."""

# Import main components
from .main import mcp

# Import models and utilities
from .models import ElementInput, RelationshipInput, DiagramInput
from .main import mcp

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
    "create_archimate_diagram",
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