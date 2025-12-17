"""Physical layer ArchiMate elements."""

from .abstract.implementation import ImplementationLayerElement
from .base import ArchiMateLayer


class PhysicalElement(ImplementationLayerElement):
    """Base class for Physical layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.PHYSICAL