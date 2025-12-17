"""Abstract base class for implementation and physical layers (Implementation, Physical)."""

from abc import ABC
from typing import Optional
from ..base import ArchiMateElement, ArchiMateLayer


class ImplementationLayerElement(ArchiMateElement, ABC):
    """Abstract base class for implementation and physical layer elements.

    This includes Implementation and Physical layers which represent the
    concrete realization and physical infrastructure of enterprise architecture.
    """

    def __init__(self, **data):
        """Initialize implementation layer element with validation."""
        super().__init__(**data)
        self._validate_implementation_layer()

    def _validate_implementation_layer(self) -> None:
        """Validate that this element belongs to an implementation layer."""
        implementation_layers = {ArchiMateLayer.IMPLEMENTATION, ArchiMateLayer.PHYSICAL}
        if self.layer not in implementation_layers:
            raise ValueError(f"ImplementationLayerElement must have layer in {implementation_layers}, got {self.layer}")

    def get_implementation_context(self) -> str:
        """Get implementation context description for this layer element."""
        contexts = {
            ArchiMateLayer.IMPLEMENTATION: "implementation projects and deliverables",
            ArchiMateLayer.PHYSICAL: "physical infrastructure and facilities"
        }
        return contexts.get(self.layer, "implementation context")