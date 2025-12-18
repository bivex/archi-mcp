# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:37:30
# Last Updated: 2025-12-18T11:37:30
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Abstract base class for supporting governance layers (Motivation, Strategy)."""

from abc import ABC
from typing import Optional
from ..base import ArchiMateElement, ArchiMateLayer


class SupportingLayerElement(ArchiMateElement, ABC):
    """Abstract base class for supporting governance layer elements.

    This includes Motivation and Strategy layers which provide governance,
    direction, and rationale for enterprise architecture.
    """

    def __init__(self, **data):
        """Initialize supporting layer element with validation."""
        super().__init__(**data)
        self._validate_supporting_layer()

    def _validate_supporting_layer(self) -> None:
        """Validate that this element belongs to a supporting governance layer."""
        supporting_layers = {ArchiMateLayer.MOTIVATION, ArchiMateLayer.STRATEGY}
        if self.layer not in supporting_layers:
            raise ValueError(f"SupportingLayerElement must have layer in {supporting_layers}, got {self.layer}")

    def get_governance_context(self) -> str:
        """Get governance context description for this supporting layer element."""
        contexts = {
            ArchiMateLayer.MOTIVATION: "motivational drivers and requirements",
            ArchiMateLayer.STRATEGY: "strategic capabilities and resources"
        }
        return contexts.get(self.layer, "governance context")