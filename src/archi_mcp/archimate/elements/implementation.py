# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:52
# Last Updated: 2025-12-18T11:40:52
#
# Licensed under the MIT License.
# Commercial licensing available upon request.


"""Implementation layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class ImplementationElement(ArchiMateElement):
    """Base class for Implementation layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.IMPLEMENTATION