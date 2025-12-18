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

__all__ = ['create_archimate_diagram', 'create_diagram_from_file', 'test_groups_functionality']

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
    • Sprites in Stereotypes: Use custom PlantUML sprites with `$sprite_name` syntax (e.g., `<<$businessProcess>>`) for visual stereotypes.
    • JSON Data Display: Embed JSON data objects in diagrams with automatic `allowmixing` directive for mixed diagram types.
    • Advanced Hide/Remove System: Use `$tags` for selective element visibility control with `hide $tag` and `remove $tag` operations. Also supports `hide_unlinked` and `remove_unlinked` for automatic handling of elements without relationships, and `remove_all_tagged` for wildcard removal of all tagged elements with selective restore.
    • Long Descriptions: Multi-line component descriptions using bracket syntax `[long description here]` for detailed documentation.
    • Enhanced Arrow Control: Full directional control with length modifiers (1-5), line styles (solid/dashed/dotted), custom colors, orientation modes (vertical/horizontal/dot), and positioning hints (`hidden` relationships).
    • Component-Specific Styling: Advanced skinparam customization with component-style variants (`uml1`, `uml2`, `rectangle`).
    • Naming Rules: Components with names starting with '$' require an alias or tag to be hideable/removable (PlantUML limitation).

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
def test_groups_functionality() -> str:
    """Test groups functionality with nested groups and element assignments."""
    try:
        from ..models import DiagramInput, ElementInput, GroupInput, RelationshipInput

        # Create test groups including nested groups
        groups = [
            GroupInput(
                id="web_group",
                name="Web Components",
                group_type="package",
                description="Frontend web components"
            ),
            GroupInput(
                id="db_group",
                name="Database Layer",
                group_type="database",
                description="Database components"
            ),
            GroupInput(
                id="nested_folder",
                name="Data Folder",
                group_type="folder",
                parent_group_id="db_group",
                description="Nested folder inside database"
            )
        ]

        # Create test elements assigned to groups
        elements = [
            ElementInput(
                id="web_server",
                name="Web Server",
                element_type="Application_Component",
                layer="Application",
                group_id="web_group",
                description="Main web server component"
            ),
            ElementInput(
                id="api_gateway",
                name="API Gateway",
                element_type="Application_Component",
                layer="Application",
                group_id="web_group",
                description="API gateway component"
            ),
            ElementInput(
                id="mysql_db",
                name="MySQL Database",
                element_type="Technology_Artifact",
                layer="Technology",
                group_id="db_group",
                description="Primary database"
            ),
            ElementInput(
                id="data_processor",
                name="Data Processor",
                element_type="Application_Component",
                layer="Application",
                group_id="nested_folder",
                description="Component in nested folder"
            )
        ]

        # Create test relationships
        relationships = [
            RelationshipInput(
                id="web_to_db",
                from_element="web_server",
                to_element="mysql_db",
                relationship_type="Access",
                description="Web server writes to database"
            ),
            RelationshipInput(
                id="api_to_processor",
                from_element="api_gateway",
                to_element="data_processor",
                relationship_type="Serving",
                description="API serves data processor"
            )
        ]

        # Create diagram input with groups enabled
        diagram_input = DiagramInput(
            title="Groups Functionality Test",
            description="Testing named groups and nested groups functionality",
            elements=elements,
            relationships=relationships,
            groups=groups,
            layout={
                "group_by_groups": True,
                "direction": "horizontal",
                "show_legend": True
            }
        )

        # Test diagram creation
        result = create_archimate_diagram_impl(diagram_input)

        # Parse result to verify structure
        import json
        result_data = json.loads(result)

        # Validate that groups functionality worked
        success = result_data.get("success", False)
        if not success:
            return f"❌ Groups functionality test failed: {result_data.get('message', 'Unknown error')}"

        files = result_data.get("files", {})
        if not files.get("plantuml") or not files.get("png"):
            return "❌ Groups functionality test failed: Missing output files"

        return "✅ **Groups Functionality Test Passed**\n\n" + \
               f"**Test Results:**\n" + \
               f"• Groups created: {len(groups)} (including {sum(1 for g in groups if g.parent_group_id)} nested)\n" + \
               f"• Elements assigned: {len(elements)}\n" + \
               f"• Relationships created: {len(relationships)}\n" + \
               f"• PlantUML file: {files.get('plantuml', 'N/A')}\n" + \
               f"• PNG file: {files.get('png', 'N/A')}\n\n" + \
               "**Features Tested:**\n" + \
               "• Named groups (package, database, folder)\n" + \
               "• Nested groups hierarchy\n" + \
               "• Element-to-group assignments\n" + \
               "• Group-based layout rendering\n" + \
               "• Relationship preservation within groups"

    except Exception as e:
        logger.error(f"Error testing groups functionality: {e}")
        return f"❌ Error testing groups functionality:\n\n{str(e)}"