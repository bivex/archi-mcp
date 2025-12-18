# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:31
# Last Updated: 2025-12-18T11:40:31
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Server configuration and environment variable management."""

import os
from typing import Any, Optional


# Environment variable defaults - only essential layout parameters
ENV_DEFAULTS = {
    # Layout Settings (these are the only configurable parameters)
    "ARCHI_MCP_DEFAULT_DIRECTION": "vertical",
    "ARCHI_MCP_DEFAULT_SHOW_LEGEND": "false",
    "ARCHI_MCP_DEFAULT_SHOW_TITLE": "false",
    "ARCHI_MCP_DEFAULT_GROUP_BY_LAYER": "true",
    "ARCHI_MCP_DEFAULT_SPACING": "compact",

    # Display Settings
    "ARCHI_MCP_DEFAULT_SHOW_ELEMENT_TYPES": "false",
    "ARCHI_MCP_DEFAULT_SHOW_RELATIONSHIP_LABELS": "true",

    # Logging Settings
    "ARCHI_MCP_LOG_LEVEL": "INFO"
}


def get_env_setting(key: str) -> str:
    """Get environment setting with fallback to default."""
    return os.getenv(key, ENV_DEFAULTS.get(key, ""))


def is_config_locked(key: str) -> bool:
    """Check if environment variable is locked by config (cannot be overridden by client)."""
    return os.getenv(key) is not None


def get_layout_setting(key: str, client_value=None):
    """Get layout setting with client override support."""
    if client_value is not None and not is_config_locked(key):
        return client_value
    return get_env_setting(key)


def get_layout_parameters_info():
    """Get information about available layout parameters for documentation."""
    return {
        "parameters": {
            "direction": {
                "type": "string",
                "enum": ["vertical", "horizontal"],
                "default": get_env_setting("ARCHI_MCP_DEFAULT_DIRECTION"),
                "description": "Diagram layout direction",
                "configurable": not is_config_locked("ARCHI_MCP_DEFAULT_DIRECTION")
            },
            "show_legend": {
                "type": "boolean",
                "default": get_env_setting("ARCHI_MCP_DEFAULT_SHOW_LEGEND").lower() == "true",
                "description": "Show legend in diagram",
                "configurable": not is_config_locked("ARCHI_MCP_DEFAULT_SHOW_LEGEND")
            },
            "show_title": {
                "type": "boolean",
                "default": get_env_setting("ARCHI_MCP_DEFAULT_SHOW_TITLE").lower() == "true",
                "description": "Show title in diagram",
                "configurable": not is_config_locked("ARCHI_MCP_DEFAULT_SHOW_TITLE")
            },
            "group_by_layer": {
                "type": "boolean",
                "default": get_env_setting("ARCHI_MCP_DEFAULT_GROUP_BY_LAYER").lower() == "true",
                "description": "Group elements by ArchiMate layer",
                "configurable": not is_config_locked("ARCHI_MCP_DEFAULT_GROUP_BY_LAYER")
            },
            "spacing": {
                "type": "string",
                "enum": ["compact", "normal", "loose"],
                "default": get_env_setting("ARCHI_MCP_DEFAULT_SPACING"),
                "description": "Spacing between diagram elements",
                "configurable": not is_config_locked("ARCHI_MCP_DEFAULT_SPACING")
            },
            "show_element_types": {
                "type": "boolean",
                "default": get_env_setting("ARCHI_MCP_DEFAULT_SHOW_ELEMENT_TYPES").lower() == "true",
                "description": "Show element type labels",
                "configurable": not is_config_locked("ARCHI_MCP_DEFAULT_SHOW_ELEMENT_TYPES")
            },
            "show_relationship_labels": {
                "type": "boolean",
                "default": get_env_setting("ARCHI_MCP_DEFAULT_SHOW_RELATIONSHIP_LABELS").lower() == "true",
                "description": "Show relationship labels",
                "configurable": not is_config_locked("ARCHI_MCP_DEFAULT_SHOW_RELATIONSHIP_LABELS")
            }
        },
        "config_locked": {
            key: is_config_locked(key)
            for key in ENV_DEFAULTS.keys()
        },
        "client_configurable": {
            key: not is_config_locked(key)
            for key in ENV_DEFAULTS.keys()
        }
    }