# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18 11:23
# Last Updated: 2025-12-18 11:23
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""ArchiMate XML Exchange Format Templates

Provides XML templates and examples for ArchiMate Exchange format.
Helps with understanding the expected XML structure.
"""

# Re-export from the new modular structure for backward compatibility
from .generators.templates import XMLTemplateGenerator as XMLTemplates
from .generators.types_info import ArchiMateTypesInfo

# Add the get_supported_element_types method to XMLTemplates for backward compatibility
XMLTemplates.get_supported_element_types = staticmethod(ArchiMateTypesInfo.get_supported_element_types)
XMLTemplates.get_supported_relationship_types = staticmethod(ArchiMateTypesInfo.get_supported_relationship_types)