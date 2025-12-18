"""MCP server models and data structures."""

import uuid
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
    group_id: Optional[str] = Field(None, description="ID of the group this element belongs to")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties")

    @model_validator(mode='after')
    def validate_layer_and_aspect(self) -> 'ElementInput':
        """Validate that layer and aspect are compatible. Auto-corrects case sensitivity."""
        valid_layers = {"Business", "Application", "Technology", "Physical", "Motivation", "Strategy", "Implementation"}
        valid_aspects = {"Active Structure", "Passive Structure", "Behavior"}

        # Auto-correct layer case (case-insensitive matching)
        layer_lower_map = {layer.lower(): layer for layer in valid_layers}
        if self.layer.lower() in layer_lower_map:
            self.layer = layer_lower_map[self.layer.lower()]
        else:
            raise ValueError(f"Invalid layer '{self.layer}'. Valid layers (case-insensitive): {sorted(valid_layers)}")

        # Auto-correct aspect case if provided
        if self.aspect:
            aspect_lower_map = {aspect.lower(): aspect for aspect in valid_aspects}
            if self.aspect.lower() in aspect_lower_map:
                self.aspect = aspect_lower_map[self.aspect.lower()]
            else:
                raise ValueError(f"Invalid aspect '{self.aspect}'. Valid aspects (case-insensitive): {sorted(valid_aspects)}")

        return self


class RelationshipInput(BaseModel):
    """Input model for ArchiMate relationships in MCP requests."""

    id: str = Field(..., description="Unique identifier for the relationship")
    from_element: str = Field(..., description="Source element ID")
    to_element: str = Field(..., description="Target element ID")
    relationship_type: str = Field(..., description="ArchiMate relationship type (e.g., 'Serving', 'Realization')")
    direction: Optional[str] = Field(None, description="Optional direction (Up, Down, Left, Right)")
    length: Optional[int] = Field(None, description="Arrow length modifier (1-5)")
    line_style: str = Field("solid", description="Line style: solid, dashed, dotted")
    color: Optional[str] = Field(None, description="Custom color for this relationship")
    orientation: str = Field("vertical", description="Arrow orientation: vertical, horizontal, dot")
    positioning: Optional[str] = Field(None, description="Advanced positioning hints (e.g., 'hidden')")
    description: Optional[str] = Field(None, description="Relationship description")
    label: Optional[str] = Field(None, description="Custom relationship label")

    @model_validator(mode='before')
    @classmethod
    def validate_and_normalize_relationship_input(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Map 'source' to 'from_element'
            if 'source' in data and 'from_element' not in data:
                data['from_element'] = data.pop('source')
            # Map 'target' to 'to_element'
            if 'target' in data and 'to_element' not in data:
                data['to_element'] = data.pop('target')
            # Map 'type' to 'relationship_type'
            if 'type' in data and 'relationship_type' not in data:
                data['relationship_type'] = data.pop('type')
            # Generate a unique ID if not provided
            if 'id' not in data or not data['id']:
                data['id'] = str(uuid.uuid4())
        return data

    @model_validator(mode='after')
    def validate_relationship_type(self) -> 'RelationshipInput':
        """Validate relationship type. Auto-corrects case sensitivity."""
        valid_types = {
            "Access", "Aggregation", "Assignment", "Association", "Composition",
            "Flow", "Influence", "Realization", "Serving", "Specialization", "Triggering"
        }

        # Auto-correct relationship type case (case-insensitive matching)
        type_lower_map = {rtype.lower(): rtype for rtype in valid_types}
        if self.relationship_type.lower() in type_lower_map:
            self.relationship_type = type_lower_map[self.relationship_type.lower()]
        else:
            raise ValueError(f"Invalid relationship type '{self.relationship_type}'. Valid types (case-insensitive): {sorted(valid_types)}")

        # Auto-correct direction case if provided
        if self.direction:
            direction_lower_map = {d.lower(): d for d in {"Up", "Down", "Left", "Right"}}
            if self.direction.lower() in direction_lower_map:
                self.direction = direction_lower_map[self.direction.lower()]
            else:
                raise ValueError(f"Invalid direction '{self.direction}'. Valid directions (case-insensitive): Up, Down, Left, Right")

        if self.length is not None and not (1 <= self.length <= 5):
            raise ValueError(f"Invalid length '{self.length}'. Length must be between 1 and 5")

        if self.line_style not in {"solid", "dashed", "dotted"}:
            raise ValueError(f"Invalid line_style '{self.line_style}'. Valid styles: solid, dashed, dotted")

        if self.orientation not in {"vertical", "horizontal", "dot"}:
            raise ValueError(f"Invalid orientation '{self.orientation}'. Valid orientations: vertical, horizontal, dot")

        return self


class GroupInput(BaseModel):
    """Input model for ArchiMate groups in MCP requests."""

    id: str = Field(..., description="Unique identifier for the group")
    name: str = Field(..., description="Display name of the group")
    group_type: str = Field(..., description="Type of grouping construct (package, node, folder, frame, cloud, database, rectangle)")
    parent_group_id: Optional[str] = Field(None, description="ID of parent group for nested groups")
    description: Optional[str] = Field(None, description="Group description")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties")

    @model_validator(mode='after')
    def validate_group_type(self) -> 'GroupInput':
        """Validate group type."""
        valid_types = {"package", "node", "folder", "frame", "cloud", "database", "rectangle"}

        if self.group_type not in valid_types:
            raise ValueError(f"Invalid group type '{self.group_type}'. Valid types: {valid_types}")

        return self


class DiagramInput(BaseModel):
    """Input model for complete ArchiMate diagrams in MCP requests."""

    title: Optional[str] = Field(None, description="Diagram title")
    description: Optional[str] = Field(None, description="Diagram description")
    elements: List[ElementInput] = Field(default_factory=list, description="List of elements in the diagram")
    relationships: List[RelationshipInput] = Field(default_factory=list, description="List of relationships in the diagram")
    groups: List[GroupInput] = Field(default_factory=list, description="List of named groups in the diagram")
    layout: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Layout configuration")

    @model_validator(mode='after')
    def validate_diagram_integrity(self) -> 'DiagramInput':
        """Validate diagram integrity - ensure all referenced elements and groups exist."""
        element_ids = {elem.id for elem in self.elements}
        group_ids = {group.id for group in self.groups}

        # Validate relationships reference existing elements
        for rel in self.relationships:
            if rel.from_element not in element_ids:
                raise ValueError(f"Relationship '{rel.id}' references unknown source element '{rel.from_element}'")
            if rel.to_element not in element_ids:
                raise ValueError(f"Relationship '{rel.id}' references unknown target element '{rel.to_element}'")

        # Validate elements reference existing groups
        for elem in self.elements:
            if elem.group_id and elem.group_id not in group_ids:
                raise ValueError(f"Element '{elem.id}' references unknown group '{elem.group_id}'")

        # Validate groups reference existing parent groups
        for group in self.groups:
            if group.parent_group_id and group.parent_group_id not in group_ids:
                raise ValueError(f"Group '{group.id}' references unknown parent group '{group.parent_group_id}'")

        return self