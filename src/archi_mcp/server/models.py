"""MCP server models and data structures."""

from pydantic import BaseModel, Field, model_validator
from typing import Any, Dict, List, Optional, Literal, Union


class ElementInput(BaseModel):
    """Input model for ArchiMate elements in MCP requests."""

    id: str = Field(..., description="Unique identifier for the element")
    name: str = Field(..., description="Display name of the element")
    element_type: str = Field(..., description="ArchiMate element type (e.g., 'Business_Actor', 'Application_Component')")
    layer: str = Field(..., description="ArchiMate layer (Business, Application, Technology, Physical, Motivation, Strategy, Implementation)")
    aspect: Optional[str] = Field(None, description="ArchiMate aspect (Active Structure, Passive Structure, Behavior)")
    description: Optional[str] = Field(None, description="Element description")
    stereotype: Optional[str] = Field(None, description="Element stereotype")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties")

    @model_validator(mode='after')
    def validate_layer_and_aspect(self) -> 'ElementInput':
        """Validate that layer and aspect are compatible."""
        valid_layers = {"Business", "Application", "Technology", "Physical", "Motivation", "Strategy", "Implementation"}
        valid_aspects = {"Active Structure", "Passive Structure", "Behavior"}

        if self.layer not in valid_layers:
            raise ValueError(f"Invalid layer '{self.layer}'. Valid layers: {valid_layers}")

        if self.aspect and self.aspect not in valid_aspects:
            raise ValueError(f"Invalid aspect '{self.aspect}'. Valid aspects: {valid_aspects}")

        return self


class RelationshipInput(BaseModel):
    """Input model for ArchiMate relationships in MCP requests."""

    id: str = Field(..., description="Unique identifier for the relationship")
    from_element: str = Field(..., description="Source element ID")
    to_element: str = Field(..., description="Target element ID")
    relationship_type: str = Field(..., description="ArchiMate relationship type (e.g., 'Serving', 'Realization')")
    direction: Optional[str] = Field(None, description="Optional direction (Up, Down, Left, Right)")
    description: Optional[str] = Field(None, description="Relationship description")
    label: Optional[str] = Field(None, description="Custom relationship label")

    @model_validator(mode='after')
    def validate_relationship_type(self) -> 'RelationshipInput':
        """Validate relationship type."""
        valid_types = {
            "Access", "Aggregation", "Assignment", "Association", "Composition",
            "Flow", "Influence", "Realization", "Serving", "Specialization", "Triggering"
        }

        if self.relationship_type not in valid_types:
            raise ValueError(f"Invalid relationship type '{self.relationship_type}'. Valid types: {valid_types}")

        if self.direction and self.direction not in {"Up", "Down", "Left", "Right"}:
            raise ValueError(f"Invalid direction '{self.direction}'. Valid directions: Up, Down, Left, Right")

        return self


class DiagramInput(BaseModel):
    """Input model for complete ArchiMate diagrams in MCP requests."""

    title: Optional[str] = Field(None, description="Diagram title")
    description: Optional[str] = Field(None, description="Diagram description")
    elements: List[ElementInput] = Field(default_factory=list, description="List of elements in the diagram")
    relationships: List[RelationshipInput] = Field(default_factory=list, description="List of relationships in the diagram")
    layout: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Layout configuration")

    @model_validator(mode='after')
    def validate_diagram_integrity(self) -> 'DiagramInput':
        """Validate diagram integrity - ensure all referenced elements exist."""
        element_ids = {elem.id for elem in self.elements}

        for rel in self.relationships:
            if rel.from_element not in element_ids:
                raise ValueError(f"Relationship '{rel.id}' references unknown source element '{rel.from_element}'")
            if rel.to_element not in element_ids:
                raise ValueError(f"Relationship '{rel.id}' references unknown target element '{rel.to_element}'")

        return self