# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:48
# Last Updated: 2025-12-18T11:40:48
#
# Licensed under the MIT License.
# Commercial licensing available upon request.


"""Relationship classification utilities."""

from typing import Set
from .types import ArchiMateRelationshipType


class RelationshipClassifier:
    """Utility class for classifying ArchiMate relationships."""

    @staticmethod
    def get_structural_relationships() -> Set[str]:
        """Get relationships that define structural composition."""
        return {ArchiMateRelationshipType.COMPOSITION, ArchiMateRelationshipType.AGGREGATION}

    @staticmethod
    def get_dynamic_relationships() -> Set[str]:
        """Get relationships that represent dynamic behavior."""
        return {ArchiMateRelationshipType.FLOW, ArchiMateRelationshipType.TRIGGERING, ArchiMateRelationshipType.ASSIGNMENT}

    @staticmethod
    def get_dependency_relationships() -> Set[str]:
        """Get relationships that represent dependencies."""
        return {ArchiMateRelationshipType.SERVING, ArchiMateRelationshipType.ACCESS, ArchiMateRelationshipType.INFLUENCE, ArchiMateRelationshipType.REALIZATION}

    @staticmethod
    def classify_relationship(relationship_type: str) -> str:
        """Classify a relationship type into its category."""
        if relationship_type in RelationshipClassifier.get_structural_relationships():
            return "structural"
        elif relationship_type in RelationshipClassifier.get_dynamic_relationships():
            return "dynamic"
        elif relationship_type in RelationshipClassifier.get_dependency_relationships():
            return "dependency"
        else:
            return "general"