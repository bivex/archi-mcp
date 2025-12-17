"""Application layer ArchiMate elements."""

from .abstract.core import CoreLayerElement
from .base import ArchiMateLayer


class ApplicationElement(CoreLayerElement):
    """Base class for Application layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.APPLICATION