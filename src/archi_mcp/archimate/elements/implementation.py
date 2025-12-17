"""Implementation layer ArchiMate elements."""

from .abstract.implementation import ImplementationLayerElement
from .base import ArchiMateLayer


class ImplementationElement(ImplementationLayerElement):
    """Base class for Implementation layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.IMPLEMENTATION