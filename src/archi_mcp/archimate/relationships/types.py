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