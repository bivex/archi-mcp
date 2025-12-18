# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:50
# Last Updated: 2025-12-18T11:40:50
#
# Licensed under the MIT License.
# Commercial licensing available upon request.


"""Strategy layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class StrategyElement(ArchiMateElement):
    """Base class for Strategy layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.STRATEGY