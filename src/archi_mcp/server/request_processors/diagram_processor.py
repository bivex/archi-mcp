# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:34
# Last Updated: 2025-12-18T11:40:34
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

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
from typing import Dict, List, Optional, TYPE_CHECKING, Any
from fastmcp import FastMCP, Context

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
from ..response_models import DiagramGenerationResponse, GroupsTestResponse, DiagramFiles, DiagramEnhancementRequest


def _enhance_validation_error(error_msg: str, diagram_data: dict) -> str:
    """Enhance validation error messages with helpful guidance."""
    enhanced_msg = error_msg

    # Check for common missing field errors
    enhanced_msg = _add_field_validation_tips(enhanced_msg, error_msg)

    # Check for note definition issues
    enhanced_msg = _add_note_validation_tips(enhanced_msg, error_msg, diagram_data)

    # Check for case sensitivity issues
    enhanced_msg = _add_case_sensitivity_tips(enhanced_msg, error_msg)

    return enhanced_msg


def _add_field_validation_tips(enhanced_msg: str, error_msg: str) -> str:
    """Add tips for common missing field errors."""
    error_lower = error_msg.lower()

    if "id" in error_lower and "required" in error_lower:
        enhanced_msg += "\n\n💡 TIP: Each element needs a unique 'id' field. Example:\n" \
                       '{"id": "web_server", "name": "Web Server", "element_type": "Application_Component", "layer": "Application"}'

    if "element_type" in error_lower and "required" in error_lower:
        enhanced_msg += "\n\n💡 TIP: Elements need an 'element_type' field. Common types:\n" \
                       "• Business: Business_Actor, Business_Process, Business_Function\n" \
                       "• Application: Application_Component, Application_Function\n" \
                       "• Technology: Technology_Node, Technology_SystemSoftware"

    if "layer" in error_lower and "required" in error_lower:
        enhanced_msg += "\n\n💡 TIP: Elements need a 'layer' field (case-insensitive). Valid layers:\n" \
                       "Business, Application, Technology, Physical, Motivation, Strategy, Implementation"

    if "relationship_type" in error_lower and "required" in error_lower:
        enhanced_msg += "\n\n💡 TIP: Relationships need a 'relationship_type' field (case-insensitive). Common types:\n" \
                       "Serving, Realization, Access, Composition, Aggregation, Assignment"

    return enhanced_msg


def _add_note_validation_tips(enhanced_msg: str, error_msg: str, diagram_data: dict) -> str:
    """Add tips for note definition issues."""
    if "note" in error_msg.lower() or "notes" in diagram_data.get("elements", []):
        elements = diagram_data.get("elements", [])
        for elem in elements:
            if elem.get("element_type") == "Note" or elem.get("name", "").lower() == "note":
                enhanced_msg += "\n\n💡 TIP: Notes should be defined within elements, not as separate elements.\n" \
                               "Correct way:\n" \
                               '{"id": "component1", "name": "My Component", "element_type": "Application_Component", "layer": "Application",\n' \
                               ' "notes": [{"content": "This is a note", "position": "right"}]}\n\n' \
                               "NOT as separate elements with relationships!"
    return enhanced_msg


def _add_case_sensitivity_tips(enhanced_msg: str, error_msg: str) -> str:
    """Add tips for case sensitivity issues."""
    error_lower = error_msg.lower()

    if "invalid layer" in error_lower:
        enhanced_msg += "\n\n💡 NOTE: Layer names are now case-insensitive and auto-corrected."

    if "invalid relationship type" in error_lower:
        enhanced_msg += "\n\n💡 NOTE: Relationship types are now case-insensitive and auto-corrected."

    return enhanced_msg

# Make DiagramInput available globally for MCP decorators
globals()['DiagramInput'] = DiagramInput

__all__ = ['create_archimate_diagram', 'create_diagram_from_file', 'test_groups_functionality', 'enhance_diagram_with_feedback', 'list_available_resources', 'create_diagram_from_template']

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
def create_archimate_diagram(diagram: dict) -> DiagramGenerationResponse:
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
    • Note Definition: Notes must be defined within element objects using the 'notes' array, not as separate elements. Example: {"id": "comp1", "notes": [{"content": "Important note", "position": "right"}]}

    Args:
        diagram: A `DiagramInput` object containing the specification for the diagram.
                 This includes elements, relationships, layout, and output configurations.

    Returns:
        A DiagramGenerationResponse object containing the generated PlantUML code and paths to exported images (PNG, SVG).

    Raises:
        ArchiMateError: If diagram generation or validation fails.
    """
    try:
        # Convert dictionary to DiagramInput object
        diagram_input = DiagramInput.model_validate(diagram)
        return create_archimate_diagram_impl(diagram_input)
    except Exception as e:
        logger.error(f"Error creating ArchiMate diagram: {e}")
        enhanced_error = _enhance_validation_error(str(e), diagram)
        raise ArchiMateError(f"Failed to create ArchiMate diagram: {enhanced_error}")


@mcp.tool()
def create_diagram_from_file(file_path: str) -> DiagramGenerationResponse:
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
def test_groups_functionality() -> GroupsTestResponse:
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
        success = result.success
        if not success:
            return GroupsTestResponse(
                success=False,
                message=f"Groups functionality test failed: {result.message}",
                groups_created=0,
                elements_assigned=0,
                relationships_created=0,
                nested_groups=0,
                files=DiagramFiles(plantuml="", png=""),
                features_tested=[]
            )

        if not result.files.plantuml or not result.files.png:
            return GroupsTestResponse(
                success=False,
                message="Groups functionality test failed: Missing output files",
                groups_created=0,
                elements_assigned=0,
                relationships_created=0,
                nested_groups=0,
                files=DiagramFiles(plantuml="", png=""),
                features_tested=[]
            )

        return GroupsTestResponse(
            success=True,
            message="Groups Functionality Test Passed",
            groups_created=len(groups),
            elements_assigned=len(elements),
            relationships_created=len(relationships),
            nested_groups=sum(1 for g in groups if g.parent_group_id),
            files=result.files,
            features_tested=[
                "Named groups (package, database, folder)",
                "Nested groups hierarchy",
                "Element-to-group assignments",
                "Group-based layout rendering",
                "Relationship preservation within groups"
            ]
        )

    except Exception as e:
        logger.error(f"Error testing groups functionality: {e}")
        return GroupsTestResponse(
            success=False,
            message=f"Error testing groups functionality: {str(e)}",
            groups_created=0,
            elements_assigned=0,
            relationships_created=0,
            nested_groups=0,
            files=DiagramFiles(plantuml="", png=""),
            features_tested=[]
        )


@mcp.tool()
def list_available_resources() -> str:
    """List all available MCP resources for ArchiMate diagram generation."""
    resources = {
        "archi://elements": "Available ArchiMate elements organized by layer and aspect",
        "archi://relationships": "Available ArchiMate relationship types",
        "archi://themes": "Available visual themes for diagram generation",
        "archi://languages": "Supported languages for internationalization",
        "archi://templates/basic": "Basic diagram template for getting started",
        "archi://templates/layered-architecture": "Complete layered enterprise architecture template",
        "archi://help/quick-reference": "Quick reference guide for using ArchiMate MCP tools",
        "archi://examples/{example_name}": "Specific diagram examples (simple-service, microservices)",
        "archi://config/defaults": "Default configuration settings"
    }

    return json.dumps({
        "description": "Available MCP resources for ArchiMate diagram generation",
        "resources": resources,
        "usage": "Use these URIs with your MCP client to access the data",
        "count": len(resources)
    }, indent=2)


@mcp.tool()
def create_diagram_from_template(template_name: str, customizations: Optional[Dict[str, Any]] = None) -> DiagramGenerationResponse:
    """Create a diagram from a predefined template with optional customizations.

    Args:
        template_name: Name of the template ('basic' or 'layered-architecture')
        customizations: Optional dictionary with customizations (title, theme, etc.)

    Returns:
        DiagramGenerationResponse with the generated diagram
    """
    try:
        _validate_template_parameters(template_name, customizations)
        template_data = _load_template_content(template_name)
        template_data = _apply_template_customizations(template_data, customizations)
        diagram_input = DiagramInput.model_validate(template_data)
        return create_archimate_diagram_impl(diagram_input)

    except Exception as e:
        logger.error(f"Error creating diagram from template: {e}")
        raise ArchiMateError(f"Failed to create diagram from template '{template_name}': {str(e)}")


def _validate_template_parameters(template_name: str, customizations: Optional[Dict[str, Any]]):
    """Validate template parameters and customizations."""
    if template_name not in ["basic", "layered-architecture"]:
        raise ArchiMateError(f"Unknown template: {template_name}. Available: basic, layered-architecture")


def _load_template_content(template_name: str) -> dict:
    """Load and parse template content based on template name."""
    from ..resources import get_basic_diagram_template, get_layered_architecture_template

    if template_name == "basic":
        template_json = get_basic_diagram_template()
    else:  # layered-architecture
        template_json = get_layered_architecture_template()

    return json.loads(template_json)


def _apply_template_customizations(template_data: dict, customizations: Optional[Dict[str, Any]]) -> dict:
    """Apply customizations to template data."""
    if not customizations:
        return template_data

    if "title" in customizations:
        template_data["title"] = customizations["title"]
    if "description" in customizations:
        template_data["description"] = customizations["description"]
    if "theme" in customizations:
        template_data["layout"]["theme"] = customizations["theme"]
    if "direction" in customizations:
        template_data["layout"]["direction"] = customizations["direction"]

    return template_data


@mcp.tool()
async def enhance_diagram_with_feedback(ctx: Context, diagram: dict) -> DiagramGenerationResponse:
    """Generate a diagram and interactively request enhancement feedback from the user.

    This tool demonstrates FastMCP's elicitation capabilities by generating an initial
    diagram and then asking the user for feedback on potential enhancements.

    Args:
        ctx: FastMCP context for elicitation
        diagram: A DiagramInput object containing the diagram specification

    Returns:
        A DiagramGenerationResponse with the enhanced diagram
    """
    try:
        # First, generate the initial diagram
        diagram_input, initial_result = await _generate_initial_diagram(diagram)
        if not initial_result.success:
            return initial_result

        # Now elicit feedback for enhancements
        enhancement_request = await ctx.elicit(
            message="Diagram generated successfully! Would you like to enhance it with additional features?",
            response_type=DiagramEnhancementRequest
        )

        return await _handle_enhancement_action(enhancement_request, diagram_input, initial_result)

    except Exception as e:
        logger.error(f"Error in enhance_diagram_with_feedback: {e}")
        # Return a basic error response
        return DiagramGenerationResponse(
            success=False,
            message=f"Failed to enhance diagram: {str(e)}",
            export_directory="",
            files=DiagramFiles(plantuml="", png="")
        )


async def _generate_initial_diagram(diagram: dict) -> tuple:
    """Generate the initial diagram from input."""
    diagram_input = DiagramInput.model_validate(diagram)
    initial_result = create_archimate_diagram_impl(diagram_input)
    return diagram_input, initial_result


async def _handle_enhancement_action(enhancement_request, diagram_input: DiagramInput, initial_result: DiagramGenerationResponse) -> DiagramGenerationResponse:
    """Handle the user's enhancement action choice."""
    if enhancement_request.action == "accept":
        return await _apply_enhancement_feedback(enhancement_request.data, diagram_input)
    elif enhancement_request.action == "decline":
        initial_result.message = "Diagram generated (enhancement declined)"
        return initial_result
    else:  # cancel
        initial_result.message = "Diagram generated (enhancement cancelled)"
        return initial_result


async def _apply_enhancement_feedback(enhancement_data, diagram_input: DiagramInput) -> DiagramGenerationResponse:
    """Apply user feedback enhancements to the diagram."""
    # Apply enhancements based on user feedback
    enhanced_layout = diagram_input.layout or {}

    if enhancement_data.add_legend:
        enhanced_layout["show_legend"] = True

    if enhancement_data.theme_preference:
        # Map theme preference to available themes
        theme_mapping = {
            "modern": "MODERN",
            "classic": "CLASSIC",
            "colorful": "COLORFUL",
            "minimal": "MINIMAL",
            "dark": "DARK",
            "professional": "PROFESSIONAL"
        }
        if enhancement_data.theme_preference.lower() in theme_mapping:
            enhanced_layout["theme"] = theme_mapping[enhancement_data.theme_preference.lower()]

    # Create enhanced diagram input
    enhanced_diagram = diagram_input.model_copy()
    enhanced_diagram.layout = enhanced_layout
    enhanced_diagram.title = f"{diagram_input.title or 'ArchiMate Diagram'} (Enhanced)"

    if enhancement_data.additional_notes:
        enhanced_diagram.description = f"{diagram_input.description or ''}\n\nNotes: {enhancement_data.additional_notes}".strip()

    # Generate the enhanced diagram
    enhanced_result = create_archimate_diagram_impl(enhanced_diagram)
    enhanced_result.message = "Diagram enhanced with user feedback!"
    return enhanced_result