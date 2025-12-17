"""PlantUML validation and image generation utilities."""

import subprocess
import time
import platform
import os
import tempfile
from pathlib import Path
from typing import Tuple


def _setup_java_environment():
    """Setup Java environment variables for PlantUML execution."""
    # Ensure JAVA_HOME is set if we can find it
    if not os.getenv("JAVA_HOME"):
        java_path = _find_java_executable()
        if java_path and java_path != "java":
            java_home = os.path.dirname(os.path.dirname(java_path))
            os.environ["JAVA_HOME"] = java_home

    # Ensure Java bin directory is in PATH
    java_path = _find_java_executable()
    if java_path and java_path != "java":
        java_bin_dir = os.path.dirname(java_path)
        current_path = os.environ.get("PATH", "")
        if java_bin_dir not in current_path:
            os.environ["PATH"] = java_bin_dir + os.pathsep + current_path


def _validate_plantuml_renders(plantuml_code: str) -> Tuple[bool, str]:
    """Validate that PlantUML code can be rendered successfully."""
    try:
        # Setup Java environment
        _setup_java_environment()

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

            # Run PlantUML - try to find Java in common locations
            java_cmd = _find_java_executable()
            cmd = [java_cmd, '-jar', plantuml_jar, '-tpng', temp_file_path]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                env=os.environ.copy()  # Use current environment
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
        return False, "Java runtime not found. Please install Java (OpenJDK) to use PlantUML. On macOS: 'brew install openjdk'. On Ubuntu/Debian: 'sudo apt install openjdk-21-jdk'."
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        if "Unable to locate a Java Runtime" in error_msg:
            return False, "Java runtime not found. Please install Java (OpenJDK) to use PlantUML. On macOS: 'brew install openjdk'. On Ubuntu/Debian: 'sudo apt install openjdk-21-jdk'."
        return False, f"PlantUML execution failed: {error_msg}"
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


def _find_java_executable() -> str:
    """Find Java executable in common locations."""
    import shutil

    # First, try JAVA_HOME environment variable
    java_home = os.getenv("JAVA_HOME")
    if java_home:
        java_path = os.path.join(java_home, "bin", "java")
        if os.path.exists(java_path) and os.access(java_path, os.X_OK):
            try:
                result = subprocess.run([java_path, "-version"],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return java_path
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

    # Try common Java paths for macOS and Linux
    java_paths = [
        "/opt/homebrew/opt/openjdk/bin/java",          # Homebrew OpenJDK (Apple Silicon)
        "/usr/local/opt/openjdk/bin/java",             # Homebrew OpenJDK (Intel)
        "/opt/homebrew/opt/openjdk@21/bin/java",       # Homebrew OpenJDK 21
        "/opt/homebrew/opt/openjdk@17/bin/java",       # Homebrew OpenJDK 17
        "/opt/homebrew/opt/openjdk@11/bin/java",       # Homebrew OpenJDK 11
        "/usr/local/opt/openjdk@21/bin/java",          # Homebrew OpenJDK 21 (Intel)
        "/usr/local/opt/openjdk@17/bin/java",          # Homebrew OpenJDK 17 (Intel)
        "/usr/local/opt/openjdk@11/bin/java",          # Homebrew OpenJDK 11 (Intel)
        "/Library/Java/JavaVirtualMachines/openjdk.jdk/Contents/Home/bin/java",  # AdoptOpenJDK
        "/usr/bin/java",                               # System Java
        "/usr/lib/jvm/default/bin/java",               # Linux default
        "/usr/lib/jvm/java-21-openjdk/bin/java",       # Linux OpenJDK 21
        "/usr/lib/jvm/java-17-openjdk/bin/java",       # Linux OpenJDK 17
        "/usr/lib/jvm/java-11-openjdk/bin/java",       # Linux OpenJDK 11
        "java"                                         # Default PATH
    ]

    for java_path in java_paths:
        try:
            # Use shutil.which for PATH-based lookups, direct check for absolute paths
            if os.path.isabs(java_path):
                if os.path.exists(java_path) and os.access(java_path, os.X_OK):
                    # Test if Java actually works
                    result = subprocess.run([java_path, "-version"],
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        return java_path
            else:
                # For PATH-based names like "java"
                found_path = shutil.which(java_path)
                if found_path:
                    # Test if Java actually works
                    result = subprocess.run([found_path, "-version"],
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        return found_path
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue

    # Last resort: try to find java in common directories
    import glob
    for pattern in [
        "/usr/lib/jvm/*/bin/java",
        "/Library/Java/JavaVirtualMachines/*/Contents/Home/bin/java",
        "/opt/homebrew/Cellar/openjdk/*/bin/java"
    ]:
        matches = glob.glob(pattern)
        for match in matches:
            if os.path.exists(match) and os.access(match, os.X_OK):
                try:
                    result = subprocess.run([match, "-version"],
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        return match
                except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                    continue

    return "java"  # Fallback to PATH


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