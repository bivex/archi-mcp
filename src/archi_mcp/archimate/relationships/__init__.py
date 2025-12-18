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

"""ArchiMate relationship types and utilities."""

from .types import ArchiMateRelationshipType
from .classifier import RelationshipClassifier
from .validator import RelationshipValidator
from .model import ArchiMateRelationship, RelationshipDirection, ArrowStyle, ARCHIMATE_RELATIONSHIPS, RELATIONSHIP_ARROW_STYLES, create_relationship

# Backward compatibility alias
RelationshipType = ArchiMateRelationshipType

__all__ = [
    "ArchiMateRelationshipType",
    "RelationshipType",  # Backward compatibility
    "RelationshipClassifier",
    "RelationshipValidator",
    "ArchiMateRelationship",
    "RelationshipDirection",
    "ArrowStyle",
    "ARCHIMATE_RELATIONSHIPS",
    "create_relationship"
]