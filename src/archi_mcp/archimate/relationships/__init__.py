"""ArchiMate relationship types and utilities."""

from .types import ArchiMateRelationshipType
from .classifier import RelationshipClassifier
from .validator import RelationshipValidator
from .model import ArchiMateRelationship, RelationshipDirection, ARCHIMATE_RELATIONSHIPS, create_relationship

# Backward compatibility alias
RelationshipType = ArchiMateRelationshipType

__all__ = [
    "ArchiMateRelationshipType",
    "RelationshipType",  # Backward compatibility
    "RelationshipClassifier",
    "RelationshipValidator",
    "ArchiMateRelationship",
    "RelationshipDirection",
    "ARCHIMATE_RELATIONSHIPS",
    "create_relationship"
]