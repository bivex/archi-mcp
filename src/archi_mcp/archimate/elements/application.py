"""Application layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class ApplicationElement(ArchiMateElement):
    """Base class for Application layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.APPLICATION