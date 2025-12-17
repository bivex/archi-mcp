"""Server components for ArchiMate MCP."""

# Import main components
from .main import mcp

# Import models
from .models import ElementInput, RelationshipInput, DiagramInput

# Import server functions
from .http_server import (
    start_http_server,
    stop_http_server,
    http_server_port,
    http_server_thread,
    http_server_running,
    find_free_port,
)
from .language import translate_relationship_labels, detect_language_from_content
from .validators import ELEMENT_TYPE_MAPPING, VALID_LAYERS, VALID_RELATIONSHIPS

# Import generator and validator
from ..archimate import ArchiMateGenerator, ArchiMateValidator

# Create global generator and validator instances
generator = ArchiMateGenerator()
validator = ArchiMateValidator()

# Import diagram creation function
from .request_processors.diagram_processor import create_archimate_diagram

__all__ = [
    "mcp",
    "ElementInput",
    "RelationshipInput",
    "DiagramInput",
    "start_http_server",
    "stop_http_server",
    "http_server_port",
    "http_server_thread",
    "http_server_running",
    "find_free_port",
    "translate_relationship_labels",
    "detect_language_from_content",
    "ELEMENT_TYPE_MAPPING",
    "VALID_LAYERS",
    "VALID_RELATIONSHIPS",
    "generator",
    "validator",
    "create_archimate_diagram"
]