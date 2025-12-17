"""Diagram processing request handlers for ArchiMate MCP Server."""

from __future__ import annotations

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
from typing import Dict, List, Optional, TYPE_CHECKING
from fastmcp import FastMCP

if TYPE_CHECKING:
    from ..models import DiagramInput

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
from ..error_handler import build_enhanced_error_response
from ..export_manager import create_export_directory
from ..models import DiagramInput

# Make DiagramInput available globally for MCP decorators
globals()['DiagramInput'] = DiagramInput

__all__ = ['create_archimate_diagram', 'create_diagram_from_file']

# Import the main MCP instance
from ..main import mcp

logger = get_logger(__name__)

# Import the implementation functions directly from the diagram engine
from ..diagram_engine import create_archimate_diagram_impl, load_diagram_from_file_impl

# Ensure DiagramInput is available in global namespace for MCP decorators
import sys
current_module = sys.modules[__name__]
current_module.DiagramInput = DiagramInput


@mcp.tool()
def create_archimate_diagram(diagram: dict) -> str:
    """Generate production-ready ArchiMate diagrams with comprehensive styling and layout options.

    This is the main MCP tool for creating ArchiMate diagrams. It provides extensive capabilities
    for defining and visualizing architectural models using the ArchiMate framework with PlantUML.

    Features include:
    - Comprehensive styling with 6 visual themes (Modern, Classic, Colorful, Minimal, Dark, Professional)
    - Hierarchical grouping of elements by layers and aspects
    - Rich component diagram features (ports, interfaces, notes)
    - Advanced relationship styling with custom arrow types and directions
    - Multi-language support for element and relationship labels (English, Russian, Slovak, Ukrainian)
    - Export capabilities to PNG, SVG, and raw PlantUML code

    AVAILABLE ELEMENTS BY LAYER:
    • Business Layer: Actor, Role, Collaboration, Interface, Process, Function, Interaction, Event, Service, Object, Contract, Representation
    • Application Layer: Component, Interface, Function, Interaction, Service, Data Object
    • Technology Layer: Node, Device, System Software, Technology Interface, Technology Function, Technology Service, Artifact
    • Physical Layer: Equipment, Facility, Distribution Network, Material\n    • Motivation Layer: Stakeholder, Driver, Assessment, Goal, Outcome, Principle, Requirement, Constraint
    • Strategy Layer: Capability, Resource, Course of Action
    • Implementation Layer: Work Package, Deliverable, Implementation Event, Plateau

    VISUAL THEMES:
    • MODERN: Clean, contemporary design with blue accents.
    • CLASSIC: Traditional styling with gray tones.
    • COLORFUL: Bright, vibrant color scheme.
    • MINIMAL: Clean, minimal design with subtle styling.
    • DARK: Dark theme suitable for presentations.
    • PROFESSIONAL: Corporate styling with professional colors.

    ADVANCED FEATURES:
    • Ports & Interfaces: Define connection points and expose interfaces for components.
    • Notes: Attach descriptive notes to elements, customize position and colors.
    • Grouping Styles: Utilize various PlantUML grouping constructs: `package`, `node`, `folder`, `frame`, `cloud`, `database`, `rectangle`.
    • Relationship Styles: Control arrow appearance with `solid`, `dashed`, `dotted` lines and specific arrowheads (e.g., `COMPOSITION`, `AGGREGATION`, `SERVING`).
    • Layout Controls: Fine-tune diagram layout with direction hints (`horizontal`, `vertical`), spacing options (`compact`, `normal`, `wide`), and advanced Graphviz engine pragmas (`layout_engine`, `concentrate`, `nodesep`, `ranksep`).

    Args:
        diagram: A `DiagramInput` object containing the specification for the diagram.
                 This includes elements, relationships, layout, and output configurations.

    Returns:
        A JSON string containing the generated PlantUML code and paths to exported images (PNG, SVG).

    Raises:
        ArchiMateError: If diagram generation or validation fails.
    """
    try:
        # Convert dictionary to DiagramInput object
        diagram_input = DiagramInput.model_validate(diagram)
        return create_archimate_diagram_impl(diagram_input)
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
        return load_diagram_from_file_impl(file_path)
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