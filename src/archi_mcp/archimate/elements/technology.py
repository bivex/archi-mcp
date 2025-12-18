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

"""Technology layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class TechnologyElement(ArchiMateElement):
    """Base class for Technology layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.TECHNOLOGY