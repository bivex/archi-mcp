"""Business layer ArchiMate elements."""

from typing import List
from .abstract.core import CoreLayerElement
from .base import ArchiMateLayer, ArchiMateAspect


class BusinessElement(CoreLayerElement):
    """Base class for Business layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.BUSINESS