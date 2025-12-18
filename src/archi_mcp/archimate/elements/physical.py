# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18 11:24
# Last Updated: 2025-12-18 11:24
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Physical layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class PhysicalElement(ArchiMateElement):
    """Base class for Physical layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.PHYSICAL