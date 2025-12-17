"""Diagram processing request handlers for ArchiMate MCP Server."""

import os
import json
import tempfile
import base64
import subprocess
import time
import platform
import threading
import socket
from pathlib import Path
from typing import Dict, List, Optional
from fastmcp import FastMCP

from ...utils.logging import get_logger
from ...utils.exceptions import ArchiMateError, ArchiMateValidationError
from ...utils.json_parser import parse_json_string
from ...utils.language_detection import LanguageDetector
from ...types import (
    ArchiMateRelationshipType,
    ArchiMateLayerType,
    LayoutDirectionType,
    LayoutSpacingType,
    BooleanStringType,
)
from ...archimate import (
    ArchiMateElement,
    ArchiMateRelationship,
    ArchiMateGenerator,
    ArchiMateValidator,
    ARCHIMATE_ELEMENTS,
    ARCHIMATE_RELATIONSHIPS,
)
from ...archimate.generator import DiagramLayout
from ...archimate.elements.base import ArchiMateLayer, ArchiMateAspect
from ...i18n import ArchiMateTranslator, AVAILABLE_LANGUAGES
from ..error_handler import _build_enhanced_error_response
from ..export_manager import create_export_directory

# Import the main MCP instance
from ..main import mcp

logger = get_logger(__name__)

# Import the large implementation function from the original server.py
# This will be refactored later in the reduce-method-complexity phase
from ... import server as server_module
_create_archimate_diagram_impl = server_module._create_archimate_diagram_impl
_load_diagram_from_file_impl = server_module._load_diagram_from_file_impl


@mcp.tool()
def create_archimate_diagram(diagram: 'DiagramInput') -> str:
    """Generate production-ready ArchiMate diagrams with comprehensive capability discovery.

    This is the main MCP tool for creating ArchiMate diagrams. For full documentation
    see the implementation function _create_archimate_diagram_impl.
    """
    try:
        return _create_archimate_diagram_impl(diagram)
    except Exception as e:
        logger.error(f"Error creating ArchiMate diagram: {e}")
        raise ArchiMateError(f"Failed to create ArchiMate diagram: {str(e)}")


@mcp.tool()
def create_diagram_from_file(file_path: str) -> str:
    """Load ArchiMate diagram from JSON file and generate diagram.

    Args:
        file_path: Path to JSON file containing diagram specification.

    Returns:
        Success message with diagram details and file locations.
    """
    try:
        return _load_diagram_from_file_impl(file_path)
    except Exception as e:
        logger.error(f"Error loading diagram from file: {e}")
        return f"❌ Error loading diagram from file:\n\n{str(e)}"


@mcp.tool()
def test_element_normalization() -> str:
    """Test element type normalization across all ArchiMate layers."""
    try:
        # For now, return a placeholder message
        # This will be implemented properly when we refactor the complex methods
        return "🧪 **Element Normalization Test**\n\nTest functionality will be implemented in the next refactoring phase."
    except Exception as e:
        logger.error(f"Error testing element normalization: {e}")
        return f"❌ Error testing element normalization:\n\n{str(e)}"