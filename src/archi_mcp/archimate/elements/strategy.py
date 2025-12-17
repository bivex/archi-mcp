"""Strategy layer ArchiMate elements."""

from .abstract.supporting import SupportingLayerElement
from .base import ArchiMateLayer


class StrategyElement(SupportingLayerElement):
    """Base class for Strategy layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.STRATEGY