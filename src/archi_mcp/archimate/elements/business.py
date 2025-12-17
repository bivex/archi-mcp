"""Business layer ArchiMate elements."""

from .abstract.core import CoreLayerElement
from .base import ArchiMateLayer


class BusinessElement(CoreLayerElement):
    """Base class for Business layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.BUSINESS