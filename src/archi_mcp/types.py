"""Type definitions and enumerations for ArchiMate MCP server."""

from enum import Enum
from typing import Dict, Set

# Import relationship types from the relationships module
from .archimate.relationships.types import ArchiMateRelationshipType


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