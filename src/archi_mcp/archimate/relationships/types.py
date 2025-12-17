"""ArchiMate relationship type definitions."""

from enum import Enum


class ArchiMateRelationshipType(str, Enum):
    """Complete ArchiMate 3.2 relationship types."""

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