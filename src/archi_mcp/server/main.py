"""Main ArchiMate MCP Server implementation."""

import logging
from fastmcp import FastMCP

from ..utils.logging import setup_logging, get_logger

# Initialize MCP server
mcp = FastMCP("archi-mcp")

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Import request processors to register tools
from . import request_processors  # noqa: F401


def main():
    """Main entry point for the ArchiMate MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()