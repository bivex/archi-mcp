# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:51
# Last Updated: 2025-12-18T11:40:51
#
# Licensed under the MIT License.
# Commercial licensing available upon request.


"""Motivation layer ArchiMate elements."""

from .base import ArchiMateElement, ArchiMateLayer


class MotivationElement(ArchiMateElement):
    """Base class for Motivation layer elements."""

    layer: ArchiMateLayer = ArchiMateLayer.MOTIVATION