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