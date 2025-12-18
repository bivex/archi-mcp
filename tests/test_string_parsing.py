# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18 11:23
# Last Updated: 2025-12-18 11:23
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Test JSON string parsing for Claude Code compatibility."""

import json
import pytest
from pydantic import ValidationError
from archi_mcp.server.models import DiagramInput, ElementInput


def test_diagram_input_from_dict():
    """Test creating DiagramInput from dictionary."""
    diagram_dict = {
        "elements": [
            {
                "id": "test1",
                "name": "Test Element",
                "element_type": "Business_Actor",
                "layer": "Business"
            }
        ],
        "relationships": [],
        "title": "Test Diagram"
    }

    diagram = DiagramInput(**diagram_dict)
    assert diagram.title == "Test Diagram"
    assert len(diagram.elements) == 1
    assert diagram.elements[0].name == "Test Element"


def test_diagraminput_from_json_string():
    """Test DiagramInput can be created from JSON string (Claude Code compatibility)."""
    diagram_json = json.dumps({
        "elements": [
            {
                "id": "actor1",
                "name": "Business Actor",
                "element_type": "Business_Actor",
                "layer": "Business",
                "description": "Test actor"
            }
        ],
        "relationships": [],
        "title": "String Input Test",
        "description": "Testing JSON string parameter"
    })

    # Create DiagramInput from JSON string (this is what Claude Code will do)
    diagram = DiagramInput.model_validate_json(diagram_json)

    # Verify parsing worked
    assert isinstance(diagram, DiagramInput)
    assert diagram.title == "String Input Test"
    assert len(diagram.elements) == 1
    assert diagram.elements[0].name == "Business Actor"


def test_diagraminput_from_nested_json_string():
    """Test DiagramInput with complex nested JSON string."""
    diagram_json = json.dumps({
        "elements": [
            {
                "id": "comp1",
                "name": "Application Component",
                "element_type": "Application_Component",
                "layer": "Application",
                "description": "Complex component"
            },
            {
                "id": "node1",
                "name": "Technology Node",
                "element_type": "Node",
                "layer": "Technology"
            }
        ],
        "relationships": [
            {
                "id": "r1",
                "from_element": "comp1",
                "to_element": "node1",
                "relationship_type": "Assignment"
            }
        ],
        "title": "Complex Diagram",
        "layout": {
            "direction": "top-bottom",
            "spacing": "normal"
        }
    })

    # Create DiagramInput from complex JSON string
    diagram = DiagramInput.model_validate_json(diagram_json)

    # Verify all fields parsed correctly
    assert diagram.title == "Complex Diagram"
    assert len(diagram.elements) == 2
    assert len(diagram.relationships) == 1
    assert diagram.layout["direction"] == "top-bottom"


def test_diagraminput_passthrough():
    """Test DiagramInput objects pass through validator unchanged."""
    original = DiagramInput(
        elements=[
            ElementInput(
                id="node1",
                name="Technology Node",
                element_type="Node",
                layer="Technology"
            )
        ],
        relationships=[],
        title="DiagramInput Test"
    )

    # Validate again (should pass through unchanged)
    diagram = DiagramInput.model_validate(original)

    # Verify it's the same
    assert diagram.title == "DiagramInput Test"
    assert len(diagram.elements) == 1
    assert diagram.elements[0].name == "Technology Node"


def test_invalid_json_string_raises_error():
    """Test that invalid JSON string raises ValidationError."""
    invalid_json = '{"elements": [invalid json'

    with pytest.raises(ValidationError) as exc_info:
        DiagramInput.model_validate_json(invalid_json)

    # ValidationError is raised for invalid JSON format
    assert 'ValidationError' in str(type(exc_info.value))


def test_invalid_dict_structure_raises_error():
    """Test that JSON string with missing required fields raises ValidationError."""
    invalid_json = json.dumps({
        "title": "Missing Elements"
        # Missing required 'elements' field
    })

    with pytest.raises(ValidationError) as exc_info:
        DiagramInput.model_validate(invalid_json)

    # Pydantic will raise ValidationError for missing required field
    assert "elements" in str(exc_info.value).lower()
