# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:19
# Last Updated: 2025-12-18T11:40:19
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
ArchiMate MCP Server

A specialized MCP (Model Context Protocol) server for generating PlantUML ArchiMate diagrams
with comprehensive enterprise architecture modeling support.

This package provides:
- Full ArchiMate 3.2 specification support
- All 55+ ArchiMate elements across 7 layers
- All 12 ArchiMate relationship types
- Enterprise architecture templates and patterns
- PlantUML code generation and validation
"""

__version__ = "1.0.0"
__author__ = "Mgr. Patrik Skovajsa, Claude Code Assistant"
__email__ = ""
__license__ = "MIT"

from .server.main import mcp

__all__ = ["mcp"]