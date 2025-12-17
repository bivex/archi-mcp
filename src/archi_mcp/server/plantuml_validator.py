"""PlantUML validation and image generation utilities."""

import subprocess
import time
import platform
import os
import tempfile
from pathlib import Path
from typing import Tuple


def _validate_plantuml_renders(plantuml_code: str) -> Tuple[bool, str]:
    """Validate that PlantUML code can be rendered successfully."""
    try:
        # Find PlantUML jar
        plantuml_jar = _find_plantuml_jar()
        if not plantuml_jar:
            return False, "PlantUML JAR file not found. Please install PlantUML."

        # Create temporary file for PlantUML code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as temp_file:
            temp_file.write(plantuml_code)
            temp_file_path = temp_file.name

        try:
            # Create temporary output file
            output_file = temp_file_path.replace('.puml', '.png')

            # Run PlantUML
            cmd = ['java', '-jar', plantuml_jar, '-tpng', temp_file_path]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )

            # Check if output file was created
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                os.remove(output_file)  # Clean up
                return True, "PlantUML code renders successfully"
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown PlantUML error"
                return False, f"PlantUML rendering failed: {error_msg}"

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    except subprocess.TimeoutExpired:
        return False, "PlantUML rendering timed out (30 seconds)"
    except FileNotFoundError:
        return False, "Java runtime not found. Please install Java to use PlantUML."
    except Exception as e:
        return False, f"PlantUML validation error: {str(e)}"


def _validate_png_file(png_file_path: Path) -> Tuple[bool, str]:
    """Validate that PNG file exists and has reasonable size."""
    try:
        if not png_file_path.exists():
            return False, f"PNG file not found: {png_file_path}"

        file_size = png_file_path.stat().st_size
        if file_size < 100:  # Very small file indicates error
            return False, f"PNG file too small ({file_size} bytes), likely rendering error"

        if file_size > 50 * 1024 * 1024:  # 50MB limit
            return False, f"PNG file too large ({file_size} bytes), likely rendering error"

        return True, f"PNG file valid ({file_size} bytes)"

    except Exception as e:
        return False, f"PNG validation error: {str(e)}"


def _find_plantuml_jar(debug_log: list = None) -> str:
    """Find PlantUML JAR file in common locations."""
    import tempfile

    # Common installation locations
    search_paths = [
        # User home directory
        Path.home() / "plantuml" / "plantuml.jar",
        Path.home() / ".plantuml" / "plantuml.jar",
        Path.home() / "bin" / "plantuml.jar",

        # System-wide installations
        Path("/usr/local/bin/plantuml.jar"),
        Path("/usr/bin/plantuml.jar"),
        Path("/opt/plantuml/plantuml.jar"),

        # Windows Program Files
        Path("C:/Program Files/plantuml/plantuml.jar"),
        Path("C:/Program Files (x86)/plantuml/plantuml.jar"),

        # macOS Applications
        Path("/Applications/PlantUML/plantuml.jar"),
    ]

    # Add current directory and subdirectories
    search_paths.extend([
        Path.cwd() / "plantuml.jar",
        Path.cwd() / "bin" / "plantuml.jar",
        Path.cwd() / "lib" / "plantuml.jar",
    ])

    # Check environment variable
    env_path = os.getenv("PLANTUML_JAR")
    if env_path:
        search_paths.insert(0, Path(env_path))

    for jar_path in search_paths:
        if jar_path.exists() and jar_path.is_file():
            if debug_log is not None:
                debug_log.append(f"Found PlantUML JAR: {jar_path}")
            return str(jar_path)

    # If not found, try to download it
    jar_path = _download_plantuml_jar(debug_log)
    if jar_path:
        return jar_path

    if debug_log is not None:
        debug_log.append(f"PlantUML JAR not found. Searched paths: {[str(p) for p in search_paths]}")

    return None


def _download_plantuml_jar(debug_log: list = None) -> str:
    """Download PlantUML JAR file if not found locally."""
    try:
        import urllib.request

        # Create temporary directory for JAR
        temp_dir = Path(tempfile.gettempdir()) / "archi_mcp_plantuml"
        temp_dir.mkdir(exist_ok=True)

        jar_path = temp_dir / "plantuml.jar"
        if jar_path.exists():
            if debug_log:
                debug_log.append(f"Using cached PlantUML JAR: {jar_path}")
            return str(jar_path)

        # Download from official PlantUML site
        url = "https://github.com/plantuml/plantuml/releases/download/v1.2023.13/plantuml-1.2023.13.jar"

        if debug_log:
            debug_log.append(f"Downloading PlantUML JAR from: {url}")

        with urllib.request.urlopen(url) as response:
            with open(jar_path, 'wb') as f:
                f.write(response.read())

        if debug_log:
            debug_log.append(f"Downloaded PlantUML JAR to: {jar_path}")

        return str(jar_path)

    except Exception as e:
        if debug_log:
            debug_log.append(f"Failed to download PlantUML JAR: {e}")
        return None