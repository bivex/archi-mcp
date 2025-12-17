"""Abstract base classes for ArchiMate elements to improve hierarchy."""

from .core import CoreLayerElement
from .supporting import SupportingLayerElement
from .implementation import ImplementationLayerElement

__all__ = ["CoreLayerElement", "SupportingLayerElement", "ImplementationLayerElement"]