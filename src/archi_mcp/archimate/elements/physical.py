"""Physical layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class PhysicalElement(ArchiMateElement):
    """Base class for Physical layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.PHYSICAL