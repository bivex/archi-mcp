"""Relationship validation utilities."""

from typing import List
from .types import ArchiMateRelationshipType


class RelationshipValidator:
    """Utility class for validating ArchiMate relationships."""

    @staticmethod
    def get_layer_relationships(source_layer: str, target_layer: str) -> List[str]:
        """Get valid relationships between specific layers.

        Args:
            source_layer: Source ArchiMate layer
            target_layer: Target ArchiMate layer

        Returns:
            List of valid relationship types between the layers
        """
        # Implementation would validate ArchiMate layer compatibility
        # For now, return all relationships as valid
        # TODO: Implement proper layer compatibility validation
        return [rel.value for rel in ArchiMateRelationshipType]

    @staticmethod
    def is_valid_relationship(relationship_type: str) -> bool:
        """Check if a relationship type is valid.

        Args:
            relationship_type: Relationship type to validate

        Returns:
            True if the relationship type is valid
        """
        return relationship_type in [rel.value for rel in ArchiMateRelationshipType]