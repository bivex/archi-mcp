"""Motivation layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class MotivationElement(ArchiMateElement):
    """Base class for Motivation layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.MOTIVATION