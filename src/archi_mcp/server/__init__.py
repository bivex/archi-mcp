# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18 11:24
# Last Updated: 2025-12-18 11:24
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Server components for ArchiMate MCP.

VERIFIED ✅ - PlantUML validation implemented
"""

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
from .validators import (
    ELEMENT_TYPE_MAPPING,
    VALID_LAYERS,
    VALID_RELATIONSHIPS,
    normalize_element_type,
    validate_element_input,
    normalize_layer,
    normalize_relationship_type,
    validate_relationship_name,
    validate_relationship_input,
)
from .plantuml_validator import validate_plantuml_renders
from .config import get_env_setting, is_config_locked, get_layout_setting

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
    "normalize_element_type",
    "validate_element_input",
    "normalize_layer",
    "normalize_relationship_type",
    "validate_relationship_name",
    "validate_relationship_input",
    "validate_plantuml_renders",
    "get_env_setting",
    "is_config_locked",
    "get_layout_setting",
    "generator",
    "validator",
    "create_archimate_diagram"
]