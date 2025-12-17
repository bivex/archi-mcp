"""Implementation layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class ImplementationElement(ArchiMateElement):
    """Base class for Implementation layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.IMPLEMENTATION