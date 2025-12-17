"""Business layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class BusinessElement(ArchiMateElement):
    """Base class for Business layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.BUSINESS