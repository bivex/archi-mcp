"""Test create_diagram_from_file tool."""

import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    os.system('chcp 65001 >nul 2>&1')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from archi_mcp import server


def test_load_from_corrected_example():
    """Test loading from corrected example file."""
    print("\n" + "="*80)
    print("TEST: Load from examples/flower_business_corrected.json")
    print("="*80)

    # Use the implementation function directly
    result = server._load_diagram_from_file_impl("examples/flower_business_corrected.json")

    print("\nResult (first 500 chars):")
    print(result[:500] + "...")

    # Should succeed - check for success status in JSON
    assert "❌" not in result  # No error emoji
    assert "status" in result and "success" in result
    assert "exports" in result.lower()


def test_load_nonexistent_file():
    """Test loading from non-existent file."""
    print("\n" + "="*80)
    print("TEST: Load from non-existent file")
    print("="*80)

    result = server._load_diagram_from_file_impl("nonexistent.json")

    print("\nResult:")
    print(result)

    # Should show error
    assert "❌" in result
    assert "not found" in result.lower()


def test_load_absolute_path():
    """Test loading with absolute path."""
    print("\n" + "="*80)
    print("TEST: Load with absolute path")
    print("="*80)

    # Get absolute path to example
    example_path = Path(__file__).parent.parent / "examples" / "flower_business_corrected.json"

    result = server._load_diagram_from_file_impl(str(example_path))

    print("\nResult (first 500 chars):")
    print(result[:500] + "...")

    # Should succeed - check for success status in JSON
    assert "❌" not in result  # No error emoji
    assert "status" in result and "success" in result
    assert "exports" in result.lower()


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
