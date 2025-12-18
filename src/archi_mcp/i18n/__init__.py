# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:35
# Last Updated: 2025-12-18T11:40:35
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Internationalization support for ArchiMate MCP server."""

from .translator import ArchiMateTranslator
from .languages import AVAILABLE_LANGUAGES

__all__ = ["ArchiMateTranslator", "AVAILABLE_LANGUAGES"]