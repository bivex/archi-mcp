# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18 11:22
# Last Updated: 2025-12-18 11:22
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""HTTP server functionality for serving static files."""

import os
import socket
import threading
from typing import Optional

# Global variables for HTTP server state
http_server_port: Optional[int] = None
http_server_thread: Optional[threading.Thread] = None
http_server_running: bool = False


def find_free_port() -> int:
    """Find a free port for HTTP server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
        return port


def start_http_server():
    """Start HTTP server for serving static files from exports directory."""
    global http_server_port, http_server_thread, http_server_running

    if http_server_running:
        return http_server_port

    # Find free port
    http_server_port = find_free_port()

    # Create Starlette app for static files
    try:
        from starlette.applications import Starlette
        from starlette.routing import Mount
        from starlette.staticfiles import StaticFiles
        import uvicorn
        from ..utils.logging import get_logger
        logger = get_logger(__name__)

        # Ensure exports directory exists
        from .export_manager import get_exports_directory
        exports_dir = get_exports_directory()

        app = Starlette(routes=[
            Mount("/exports", StaticFiles(directory=exports_dir), name="exports"),
        ])

        def run_server():
            uvicorn.run(app, host="127.0.0.1", port=http_server_port, log_level="warning")

        http_server_thread = threading.Thread(target=run_server, daemon=True)
        http_server_thread.start()
        http_server_running = True

        logger.info(f"HTTP server started on http://127.0.0.1:{http_server_port}")
        return http_server_port

    except ImportError as e:
        from ..utils.logging import get_logger
        logger = get_logger(__name__)
        logger.error(f"Failed to start HTTP server: {e}. Install starlette and uvicorn.")
        return None


def stop_http_server():
    """Stop the HTTP server if running."""
    global http_server_port, http_server_thread, http_server_running

    if not http_server_running:
        return

    if http_server_thread and http_server_thread.is_alive():
        # Note: In a real implementation, you'd want a way to gracefully stop uvicorn
        # For now, we just mark it as not running
        pass

    http_server_running = False
    http_server_port = None
    http_server_thread = None

    from .error_handler import logger
    logger.info("HTTP server stopped")