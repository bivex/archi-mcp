"""Technology layer ArchiMate elements."""

from .abstract.core import CoreLayerElement
from .base import ArchiMateLayer


class TechnologyElement(CoreLayerElement):
    """Base class for Technology layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.TECHNOLOGY