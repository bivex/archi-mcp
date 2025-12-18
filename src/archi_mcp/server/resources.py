# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:30
# Last Updated: 2025-12-18T11:40:30
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""MCP Resources for ArchiMate MCP Server - providing data and templates to clients."""

import json
from typing import Dict, List, Any
from fastmcp import FastMCP

from ..utils.logging import get_logger
from ..i18n import AVAILABLE_LANGUAGES
from ..archimate import (
    ARCHIMATE_ELEMENTS,
    ARCHIMATE_RELATIONSHIPS,
    ArchiMateElement,
    ArchiMateRelationship
)
from ..archimate.generator import DiagramLayout
from ..archimate.themes import DiagramTheme
from .main import mcp

logger = get_logger(__name__)


@mcp.resource("archi://elements")
def get_available_elements() -> str:
    """Get all available ArchiMate elements organized by layer and aspect."""
    elements_by_layer = {}

    for layer_name, aspects in ARCHIMATE_ELEMENTS.items():
        elements_by_layer[layer_name] = {}
        for aspect_name, elements in aspects.items():
            elements_by_layer[layer_name][aspect_name] = list(elements.keys())

    return json.dumps({
        "description": "Available ArchiMate elements organized by layer and aspect",
        "layers": elements_by_layer,
        "total_elements": sum(
            len(aspect_elements)
            for layer_aspects in ARCHIMATE_ELEMENTS.values()
            for aspect_elements in layer_aspects.values()
        )
    }, indent=2)


@mcp.resource("archi://relationships")
def get_available_relationships() -> str:
    """Get all available ArchiMate relationship types."""
    return json.dumps({
        "description": "Available ArchiMate relationship types",
        "relationships": list(ARCHIMATE_RELATIONSHIPS.keys()),
        "count": len(ARCHIMATE_RELATIONSHIPS)
    }, indent=2)


@mcp.resource("archi://themes")
def get_available_themes() -> str:
    """Get available visual themes for diagram generation."""
    # Import the get_theme_presets function directly
    from ..archimate.themes import DiagramStyling
    theme_presets = DiagramStyling.get_theme_presets()

    themes_info = {}
    for theme_enum, theme_styling in theme_presets.items():
        theme_name = theme_enum.value
        themes_info[theme_name] = {
            "description": f"{theme_name.title()} theme for ArchiMate diagrams",
            "colors": {
                "background": theme_styling.colors.background,
                "primary": theme_styling.colors.primary,
                "secondary": theme_styling.colors.secondary,
                "accent": theme_styling.colors.accent,
                "text": theme_styling.colors.text,
                "border": theme_styling.colors.border
            },
            "layer_colors": theme_styling.colors.layer_colors,
            "font": {
                "name": theme_styling.font.name if theme_styling.font else "Default",
                "size": theme_styling.font.size if theme_styling.font else 12
            } if theme_styling.font else None
        }

    return json.dumps({
        "description": "Available visual themes for ArchiMate diagrams",
        "themes": themes_info,
        "count": len(theme_presets)
    }, indent=2)


@mcp.resource("archi://languages")
def get_supported_languages() -> str:
    """Get supported languages for element and relationship labels."""
    return json.dumps({
        "description": "Supported languages for internationalization",
        "languages": list(AVAILABLE_LANGUAGES.keys()),
        "default": "en",
        "count": len(AVAILABLE_LANGUAGES)
    }, indent=2)


@mcp.resource("archi://templates/basic")
def get_basic_diagram_template() -> str:
    """Get a basic ArchiMate diagram template for getting started."""
    template = {
        "title": "Basic ArchiMate Diagram",
        "description": "A simple template to get started with ArchiMate diagrams",
        "elements": [
            {
                "id": "business_actor",
                "name": "Business User",
                "element_type": "Business_Actor",
                "layer": "Business",
                "description": "A business actor that interacts with the system"
            },
            {
                "id": "app_component",
                "name": "Application Component",
                "element_type": "Application_Component",
                "layer": "Application",
                "description": "Core application component"
            },
            {
                "id": "database",
                "name": "Database Server",
                "element_type": "Node",
                "layer": "Technology",
                "description": "Technology infrastructure"
            }
        ],
        "relationships": [
            {
                "id": "user_to_app",
                "from_element": "business_actor",
                "to_element": "app_component",
                "relationship_type": "Serving",
                "description": "Application serves business needs"
            },
            {
                "id": "app_to_db",
                "from_element": "app_component",
                "to_element": "database",
                "relationship_type": "Access",
                "description": "Application accesses database"
            }
        ],
        "layout": {
            "direction": "vertical",
            "show_legend": True,
            "theme": "modern"
        }
    }

    return json.dumps(template, indent=2)


@mcp.resource("archi://templates/layered-architecture")
def get_layered_architecture_template() -> str:
    """Get a comprehensive layered architecture template."""
    template = {
        "title": "Layered Enterprise Architecture",
        "description": "Complete layered architecture showing Business, Application, and Technology layers",
        "elements": [
            # Business Layer
            {
                "id": "customer",
                "name": "Customer",
                "element_type": "Business_Actor",
                "layer": "Business",
                "description": "External customer"
            },
            {
                "id": "sales_process",
                "name": "Sales Process",
                "element_type": "Business_Process",
                "layer": "Business",
                "description": "Sales business process"
            },
            {
                "id": "order_service",
                "name": "Order Service",
                "element_type": "Business_Service",
                "layer": "Business",
                "description": "Order management service"
            },
            # Application Layer
            {
                "id": "web_app",
                "name": "Web Application",
                "element_type": "Application_Component",
                "layer": "Application",
                "description": "Customer-facing web application"
            },
            {
                "id": "api_gateway",
                "name": "API Gateway",
                "element_type": "Application_Component",
                "layer": "Application",
                "description": "API management component"
            },
            {
                "id": "order_db",
                "name": "Order Database",
                "element_type": "Data_Object",
                "layer": "Application",
                "description": "Order data storage"
            },
            # Technology Layer
            {
                "id": "web_server",
                "name": "Web Server",
                "element_type": "Node",
                "layer": "Technology",
                "description": "Web server infrastructure"
            },
            {
                "id": "app_server",
                "name": "Application Server",
                "element_type": "Node",
                "layer": "Technology",
                "description": "Application server infrastructure"
            },
            {
                "id": "database_server",
                "name": "Database Server",
                "element_type": "Node",
                "layer": "Technology",
                "description": "Database server infrastructure"
            }
        ],
        "relationships": [
            # Business relationships
            {
                "id": "customer_uses_sales",
                "from_element": "customer",
                "to_element": "sales_process",
                "relationship_type": "Triggering",
                "description": "Customer triggers sales process"
            },
            {
                "id": "sales_realizes_service",
                "from_element": "sales_process",
                "to_element": "order_service",
                "relationship_type": "Realization",
                "description": "Sales process realizes order service"
            },
            # Application relationships
            {
                "id": "web_realizes_sales",
                "from_element": "web_app",
                "to_element": "sales_process",
                "relationship_type": "Realization",
                "description": "Web app realizes sales process"
            },
            {
                "id": "web_accesses_api",
                "from_element": "web_app",
                "to_element": "api_gateway",
                "relationship_type": "Serving",
                "description": "Web app uses API gateway"
            },
            {
                "id": "api_accesses_data",
                "from_element": "api_gateway",
                "to_element": "order_db",
                "relationship_type": "Access",
                "description": "API accesses order data"
            },
            # Technology relationships
            {
                "id": "web_server_hosts_app",
                "from_element": "web_server",
                "to_element": "web_app",
                "relationship_type": "Assignment",
                "description": "Web server hosts web application"
            },
            {
                "id": "app_server_hosts_api",
                "from_element": "app_server",
                "to_element": "api_gateway",
                "relationship_type": "Assignment",
                "description": "App server hosts API gateway"
            },
            {
                "id": "db_server_hosts_data",
                "from_element": "database_server",
                "to_element": "order_db",
                "relationship_type": "Assignment",
                "description": "DB server hosts order data"
            }
        ],
        "layout": {
            "direction": "vertical",
            "group_by_layer": True,
            "show_legend": True,
            "theme": "professional",
            "spacing": "normal"
        }
    }

    return json.dumps(template, indent=2)


@mcp.resource("archi://help/quick-reference")
def get_quick_reference() -> str:
    """Get a quick reference guide for using ArchiMate MCP tools."""
    help_content = {
        "title": "ArchiMate MCP Quick Reference",
        "description": "Essential guide for creating ArchiMate diagrams",
        "tools": {
            "create_archimate_diagram": {
                "description": "Generate ArchiMate diagrams from structured data",
                "parameters": {
                    "diagram": "DiagramInput object with elements, relationships, and layout"
                },
                "returns": "DiagramGenerationResponse with file paths and PlantUML code"
            },
            "create_diagram_from_file": {
                "description": "Load and generate diagram from JSON file",
                "parameters": {
                    "file_path": "Path to JSON file containing diagram specification"
                },
                "returns": "DiagramGenerationResponse with generated files"
            },
            "test_groups_functionality": {
                "description": "Test advanced grouping features",
                "parameters": "None",
                "returns": "GroupsTestResponse with test results"
            },
            "enhance_diagram_with_feedback": {
                "description": "Generate diagram with interactive enhancement feedback",
                "parameters": {
                    "diagram": "DiagramInput object"
                },
                "returns": "Enhanced DiagramGenerationResponse"
            }
        },
        "resources": {
            "archi://elements": "Available ArchiMate elements by layer",
            "archi://relationships": "Available relationship types",
            "archi://themes": "Visual themes for diagrams",
            "archi://languages": "Supported languages for labels",
            "archi://templates/basic": "Basic diagram template",
            "archi://templates/layered-architecture": "Complete layered architecture template",
            "archi://help/quick-reference": "This quick reference guide"
        },
        "element_layers": ["Business", "Application", "Technology", "Physical", "Motivation", "Strategy", "Implementation"],
        "tips": [
            "Use descriptive IDs for elements (e.g., 'web_server', 'customer_db')",
            "Always specify both layer and element_type for elements",
            "Relationship types are case-insensitive but will be auto-corrected",
            "Use groups to organize related elements visually",
            "Themes can significantly change diagram appearance",
            "Multi-language support available for international diagrams"
        ]
    }

    return json.dumps(help_content, indent=2)


@mcp.resource("archi://examples/{example_name}")
def get_diagram_example(example_name: str) -> str:
    """Get specific diagram examples by name."""
    examples = {
        "simple-service": {
            "title": "Simple Service Architecture",
            "description": "Basic service-oriented architecture example",
            "elements": [
                {
                    "id": "client",
                    "name": "Client Application",
                    "element_type": "Application_Component",
                    "layer": "Application"
                },
                {
                    "id": "service",
                    "name": "Business Service",
                    "element_type": "Business_Service",
                    "layer": "Business"
                },
                {
                    "id": "database",
                    "name": "Database",
                    "element_type": "Data_Object",
                    "layer": "Application"
                }
            ],
            "relationships": [
                {
                    "id": "client_uses_service",
                    "from_element": "client",
                    "to_element": "service",
                    "relationship_type": "Serving"
                },
                {
                    "id": "service_uses_db",
                    "from_element": "service",
                    "to_element": "database",
                    "relationship_type": "Access"
                }
            ]
        },
        "microservices": {
            "title": "Microservices Architecture",
            "description": "Modern microservices architecture pattern",
            "elements": [
                {
                    "id": "api_gateway",
                    "name": "API Gateway",
                    "element_type": "Application_Component",
                    "layer": "Application"
                },
                {
                    "id": "user_service",
                    "name": "User Service",
                    "element_type": "Application_Component",
                    "layer": "Application"
                },
                {
                    "id": "order_service",
                    "name": "Order Service",
                    "element_type": "Application_Component",
                    "layer": "Application"
                },
                {
                    "id": "notification_service",
                    "name": "Notification Service",
                    "element_type": "Application_Component",
                    "layer": "Application"
                }
            ],
            "relationships": [
                {
                    "id": "gateway_to_user",
                    "from_element": "api_gateway",
                    "to_element": "user_service",
                    "relationship_type": "Serving"
                },
                {
                    "id": "gateway_to_order",
                    "from_element": "api_gateway",
                    "to_element": "order_service",
                    "relationship_type": "Serving"
                },
                {
                    "id": "order_to_notification",
                    "from_element": "order_service",
                    "to_element": "notification_service",
                    "relationship_type": "Triggering"
                }
            ],
            "groups": [
                {
                    "id": "services_group",
                    "name": "Microservices",
                    "group_type": "package",
                    "description": "All microservice components"
                }
            ]
        }
    }

    if example_name not in examples:
        return json.dumps({
            "error": f"Example '{example_name}' not found",
            "available_examples": list(examples.keys())
        }, indent=2)

    example = examples[example_name]
    example["layout"] = {
        "direction": "horizontal",
        "show_legend": True,
        "theme": "modern"
    }

    return json.dumps(example, indent=2)


@mcp.resource("archi://config/defaults")
def get_default_configuration() -> str:
    """Get default configuration settings for diagram generation."""
    defaults = {
        "layout": {
            "direction": "vertical",
            "show_legend": True,
            "show_title": True,
            "group_by_layer": False,
            "spacing": "normal",
            "theme": "modern"
        },
        "export": {
            "formats": ["png", "svg", "plantuml"],
            "png_resolution": "high",
            "svg_scalable": True
        },
        "validation": {
            "strict_mode": False,
            "auto_correct_case": True,
            "validate_relationships": True
        },
        "features": {
            "multi_language": True,
            "grouping": True,
            "advanced_styling": True,
            "custom_relationships": True
        }
    }

    return json.dumps({
        "description": "Default configuration settings for ArchiMate diagram generation",
        "defaults": defaults
    }, indent=2)