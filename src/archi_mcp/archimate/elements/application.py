# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:53
# Last Updated: 2025-12-18T11:40:53
#
# Licensed under the MIT License.
# Commercial licensing available upon request.


"""Application layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class ApplicationElement(ArchiMateElement):
    """Base class for Application layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.APPLICATION