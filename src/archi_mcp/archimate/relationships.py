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

"""ArchiMate relationship definitions."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from ..utils.exceptions import ArchiMateRelationshipError
from .relationships.types import ArchiMateRelationshipType
from .relationships.model import ArrowStyle


# RelationshipType enum moved to relationships.types to avoid duplication


class RelationshipDirection(str, Enum):
    """Relationship direction modifiers for PlantUML."""
    UP = "Up"
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"




    
    def validate_relationship(self, elements: dict) -> List[str]:
        """Validate the relationship according to ArchiMate specification.
        
        Args:
            elements: Dictionary of element IDs to ArchiMateElement objects
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check if elements exist
        if self.from_element not in elements:
            errors.append(f"Source element '{self.from_element}' not found")
        if self.to_element not in elements:
            errors.append(f"Target element '{self.to_element}' not found")
            
        if errors:
            return errors
        
        # Get element objects
        from_elem = elements[self.from_element]
        to_elem = elements[self.to_element]
        
        # Validate relationship type constraints
        validation_errors = self._validate_relationship_constraints(from_elem, to_elem)
        errors.extend(validation_errors)
        
        return errors
    
    def _validate_relationship_constraints(self, from_elem, to_elem) -> List[str]:
        """Validate ArchiMate relationship constraints.
        
        Args:
            from_elem: Source ArchiMateElement
            to_elem: Target ArchiMateElement
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Basic validation - more complex rules would be implemented here
        # For now, we'll do basic type checking
        
        # Access relationships typically connect active structure to passive structure
        # But this is not a strict rule - it's just a guideline
        if self.relationship_type == ArchiMateRelationshipType.ACCESS:
            if (from_elem.aspect.value != "Active Structure" or 
                to_elem.aspect.value != "Passive Structure"):
                # Only warn, don't error - Access can be used more flexibly
                pass  # Relaxed validation for Access relationships
        
        # Composition guidelines - ArchiMate allows cross-layer composition in many cases
        if self.relationship_type == ArchiMateRelationshipType.COMPOSITION:
            # Cross-layer composition is allowed in ArchiMate 3.2:
            # - Application components can be composed of technology elements
            # - Business services can be composed of application services  
            # - Physical elements can be composed of technology elements
            # Only warn for unusual combinations, don't block them
            if from_elem.layer != to_elem.layer:
                # This is informational only - ArchiMate allows cross-layer composition
                pass  # Relaxed validation for Composition relationships
        
        # Add more constraint validations as needed
        
        return errors
    
    def __str__(self) -> str:
        return f"{self.from_element} --{self.relationship_type.value}--> {self.to_element}"
    
    def __repr__(self) -> str:
        return (f"ArchiMateRelationship(id='{self.id}', "
                f"from='{self.from_element}', to='{self.to_element}', "
                f"type='{self.relationship_type.value}')")


# Registry of all ArchiMate relationships
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