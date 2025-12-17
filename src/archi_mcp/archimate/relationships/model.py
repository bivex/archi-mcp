"""ArchiMate relationship model definitions."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from ...utils.exceptions import ArchiMateRelationshipError
from .types import ArchiMateRelationshipType


class RelationshipDirection(str, Enum):
    """Relationship direction modifiers for PlantUML."""
    UP = "Up"
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"


class ArchiMateRelationship(BaseModel):
    """ArchiMate relationship definition."""

    id: str = Field(..., description="Unique identifier for the relationship")
    from_element: str = Field(..., description="Source element ID")
    to_element: str = Field(..., description="Target element ID")
    relationship_type: ArchiMateRelationshipType = Field(..., description="Type of relationship")
    direction: Optional[RelationshipDirection] = Field(None, description="Optional direction")
    description: Optional[str] = Field(None, description="Relationship description")
    label: Optional[str] = Field(None, description="Relationship label")
    properties: dict = Field(default_factory=dict, description="Additional properties")

    def to_plantuml(self, translator=None, show_labels: bool = True) -> str:
        """Generate PlantUML code for this relationship.

        Args:
            translator: Optional translator for relationship labels
            show_labels: Whether to display relationship labels and custom names

        Returns:
            PlantUML relationship code
        """
        # Determine relationship direction
        direction_str = ""
        if self.direction:
            direction_str = f" {self.direction.value}"

        # Determine relationship label
        label = ""
        if show_labels:
            if self.label:
                label = f" : {self.label}"
            elif translator:
                # Use translated relationship type as fallback
                translated_type = translator.translate_relationship(self.relationship_type.value)
                label = f" : {translated_type}"

        # Generate PlantUML relationship
        plantuml_code = f'"{self.from_element}" --> "{self.to_element}"{direction_str}{label}'

        return plantuml_code

    def validate_relationship(self, elements: dict) -> List[str]:
        """Validate the relationship according to ArchiMate specification.

        Args:
            elements: Dictionary of element IDs to ArchiMateElement objects

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check required fields
        if not self.id:
            errors.append("Relationship ID is required")
        if not self.from_element:
            errors.append("Source element ID is required")
        if not self.to_element:
            errors.append("Target element ID is required")
        if not self.relationship_type:
            errors.append("Relationship type is required")

        # Check for self-references
        if self.from_element == self.to_element:
            errors.append("Relationship cannot reference the same element")

        # Check if referenced elements exist
        if self.from_element not in elements:
            errors.append(f"Source element '{self.from_element}' does not exist")
        if self.to_element not in elements:
            errors.append(f"Target element '{self.to_element}' does not exist")

        # If elements exist, perform additional validation
        if self.from_element in elements and self.to_element in elements:
            from_elem = elements[self.from_element]
            to_elem = elements[self.to_element]

            # Validate relationship constraints based on element types and layers
            constraint_errors = self._validate_relationship_constraints(from_elem, to_elem)
            errors.extend(constraint_errors)

        return errors

    def _validate_relationship_constraints(self, from_elem, to_elem) -> List[str]:
        """Validate relationship constraints between source and target elements.

        Args:
            from_elem: Source ArchiMateElement
            to_elem: Target ArchiMateElement

        Returns:
            List of constraint validation errors
        """
        errors = []

        # Basic layer compatibility check
        if hasattr(from_elem, 'layer') and hasattr(to_elem, 'layer'):
            # Allow relationships within the same layer or between compatible layers
            compatible_layers = {
                'Business': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Application': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Technology': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Physical': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Implementation': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Motivation': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Strategy': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy']
            }

            from_layer = str(from_elem.layer.value) if hasattr(from_elem.layer, 'value') else str(from_elem.layer)
            to_layer = str(to_elem.layer.value) if hasattr(to_elem.layer, 'value') else str(to_elem.layer)

            if to_layer not in compatible_layers.get(from_layer, []):
                errors.append(f"Invalid relationship from {from_layer} layer to {to_layer} layer")

        return errors

    def __str__(self) -> str:
        return f"{self.from_element} --{self.relationship_type.value}--> {self.to_element}"


# Relationship type mapping for backward compatibility
ARCHIMATE_RELATIONSHIPS = {
    "Access": ArchiMateRelationshipType.ACCESS,
    "Aggregation": ArchiMateRelationshipType.AGGREGATION,
    "Assignment": ArchiMateRelationshipType.ASSIGNMENT,
    "Association": ArchiMateRelationshipType.ASSOCIATION,
    "Composition": ArchiMateRelationshipType.COMPOSITION,
    "Flow": ArchiMateRelationshipType.FLOW,
    "Influence": ArchiMateRelationshipType.INFLUENCE,
    "Realization": ArchiMateRelationshipType.REALIZATION,
    "Serving": ArchiMateRelationshipType.SERVING,
    "Specialization": ArchiMateRelationshipType.SPECIALIZATION,
    "Triggering": ArchiMateRelationshipType.TRIGGERING,
}


def create_relationship(
    relationship_id: str,
    from_element: str,
    to_element: str,
    relationship_type: str,
    direction: Optional[str] = None,
    description: Optional[str] = None,
    label: Optional[str] = None,
    **kwargs
) -> ArchiMateRelationship:
    """Create an ArchiMate relationship.

    Args:
        relationship_id: Unique identifier for the relationship
        from_element: Source element ID
        to_element: Target element ID
        relationship_type: Type of relationship
        direction: Optional direction (Up, Down, Left, Right)
        description: Optional description
        label: Optional label
        **kwargs: Additional properties

    Returns:
        ArchiMateRelationship instance

    Raises:
        ArchiMateRelationshipError: If relationship type is invalid
    """
    from ...utils.exceptions import ArchiMateRelationshipError

    # Validate relationship type
    if relationship_type not in ARCHIMATE_RELATIONSHIPS:
        valid_types = list(ARCHIMATE_RELATIONSHIPS.keys())
        raise ArchiMateRelationshipError(
            f"Invalid relationship type '{relationship_type}'. "
            f"Valid types: {valid_types}",
            from_element=from_element,
            to_element=to_element,
            relationship_type=relationship_type
        )

    # Validate direction if provided
    direction_enum = None
    if direction:
        try:
            direction_enum = RelationshipDirection(direction)
        except ValueError:
            valid_directions = [d.value for d in RelationshipDirection]
            raise ArchiMateRelationshipError(
                f"Invalid direction '{direction}'. "
                f"Valid directions: {valid_directions}",
                from_element=from_element,
                to_element=to_element,
                relationship_type=relationship_type
            )

    return ArchiMateRelationship(
        id=relationship_id,
        from_element=from_element,
        to_element=to_element,
        relationship_type=ARCHIMATE_RELATIONSHIPS[relationship_type],
        direction=direction_enum,
        description=description,
        label=label,
        properties=kwargs
    )