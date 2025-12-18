# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:31:50
# Last Updated: 2025-12-18T11:31:50
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Abstract base classes for ArchiMate elements to improve hierarchy."""

from .core import CoreLayerElement
from .supporting import SupportingLayerElement
from .implementation import ImplementationLayerElement

__all__ = ["CoreLayerElement", "SupportingLayerElement", "ImplementationLayerElement"]