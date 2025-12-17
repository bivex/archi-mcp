"""Strategy layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class StrategyElement(ArchiMateElement):
    """Base class for Strategy layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.STRATEGY