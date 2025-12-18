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

"""Abstract base class for core operational layers (Business, Application, Technology)."""

from abc import ABC
from typing import Optional
from ..base import ArchiMateElement, ArchiMateLayer


class CoreLayerElement(ArchiMateElement, ABC):
    """Abstract base class for core operational layer elements.

    This includes Business, Application, and Technology layers which represent
    the operational aspects of enterprise architecture.
    """

    def __init__(self, **data):
        """Initialize core layer element with validation."""
        super().__init__(**data)
        self._validate_core_layer()

    def _validate_core_layer(self) -> None:
        """Validate that this element belongs to a core operational layer."""
        core_layers = {ArchiMateLayer.BUSINESS, ArchiMateLayer.APPLICATION, ArchiMateLayer.TECHNOLOGY}
        if self.layer not in core_layers:
            raise ValueError(f"CoreLayerElement must have layer in {core_layers}, got {self.layer}")

    def get_operational_context(self) -> str:
        """Get operational context description for this core layer element."""
        contexts = {
            ArchiMateLayer.BUSINESS: "business operations and processes",
            ArchiMateLayer.APPLICATION: "application services and components",
            ArchiMateLayer.TECHNOLOGY: "technology infrastructure and platforms"
        }
        return contexts.get(self.layer, "operational context")