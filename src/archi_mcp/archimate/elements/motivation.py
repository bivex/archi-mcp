"""Motivation layer ArchiMate elements."""

from .abstract.supporting import SupportingLayerElement
from .base import ArchiMateLayer


class MotivationElement(SupportingLayerElement):
    """Base class for Motivation layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.MOTIVATION