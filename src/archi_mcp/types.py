"""Type definitions and enumerations for ArchiMate MCP server."""

from enum import Enum
from typing import Dict, List, Set


class ArchiMateRelationshipType(str, Enum):
    """Complete ArchiMate 3.2 relationship types with descriptions and validation methods."""

    ACCESS = "Access"  # Element can access another element
    AGGREGATION = "Aggregation"  # Whole-part relationship, parts can exist independently
    ASSIGNMENT = "Assignment"  # Element is assigned to another element
    ASSOCIATION = "Association"  # General relationship between elements
    COMPOSITION = "Composition"  # Whole-part relationship, parts cannot exist independently
    FLOW = "Flow"  # Transfer of information, money, goods, etc.
    INFLUENCE = "Influence"  # Element influences another element
    REALIZATION = "Realization"  # Element realizes another element
    SERVING = "Serving"  # Element serves another element
    SPECIALIZATION = "Specialization"  # Is-a relationship, inheritance
    TRIGGERING = "Triggering"  # Element triggers another element

    @classmethod
    def get_structural_relationships(cls) -> Set[str]:
        """Get relationships that define structural composition."""
        return {cls.COMPOSITION, cls.AGGREGATION}

    @classmethod
    def get_dynamic_relationships(cls) -> Set[str]:
        """Get relationships that represent dynamic behavior."""
        return {cls.FLOW, cls.TRIGGERING, cls.ASSIGNMENT}

    @classmethod
    def get_dependency_relationships(cls) -> Set[str]:
        """Get relationships that represent dependencies."""
        return {cls.SERVING, cls.ACCESS, cls.INFLUENCE, cls.REALIZATION}

    @classmethod
    def get_layer_relationships(cls, source_layer: str, target_layer: str) -> List[str]:
        """Get valid relationships between specific layers."""
        # Implementation would validate ArchiMate layer compatibility
        # For now, return all relationships as valid
        return [rel.value for rel in cls]


class ArchiMateLayerType(str, Enum):
    """ArchiMate 3.2 specification layers with utility methods."""

    BUSINESS = "Business"
    APPLICATION = "Application"
    TECHNOLOGY = "Technology"
    PHYSICAL = "Physical"
    MOTIVATION = "Motivation"
    STRATEGY = "Strategy"
    IMPLEMENTATION = "Implementation"

    @classmethod
    def get_core_layers(cls) -> Set[str]:
        """Get the three core architectural layers."""
        return {cls.BUSINESS, cls.APPLICATION, cls.TECHNOLOGY}

    @classmethod
    def get_extension_layers(cls) -> Set[str]:
        """Get the extension layers."""
        return {cls.PHYSICAL, cls.MOTIVATION, cls.STRATEGY, cls.IMPLEMENTATION}

    @classmethod
    def get_layer_hierarchy(cls) -> Dict[str, int]:
        """Get layer hierarchy levels (higher number = more concrete)."""
        return {
            cls.STRATEGY: 1,
            cls.BUSINESS: 2,
            cls.APPLICATION: 3,
            cls.TECHNOLOGY: 4,
            cls.PHYSICAL: 5,
            cls.IMPLEMENTATION: 6,
            cls.MOTIVATION: 7,  # Cross-cutting
        }


class LayoutDirectionType(str, Enum):
    """Layout direction options for diagram generation."""

    TOP_BOTTOM = "top-bottom"
    LEFT_RIGHT = "left-right"
    BOTTOM_TOP = "bottom-top"
    RIGHT_LEFT = "right-left"


class LayoutSpacingType(str, Enum):
    """Layout spacing options for diagram generation."""

    COMPACT = "compact"
    NORMAL = "normal"
    WIDE = "wide"


class BooleanStringType(str, Enum):
    """Boolean values as strings (required for layout parameters)."""

    TRUE = "true"
    FALSE = "false"