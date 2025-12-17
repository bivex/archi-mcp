"""Technology layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class TechnologyElement(ArchiMateElement):
    """Base class for Technology layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.TECHNOLOGY