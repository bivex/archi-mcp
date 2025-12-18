"""Test script for validating the flower business diagram on Windows.

This script tests the corrected JSON against the ArchiMate MCP server
to ensure it works properly on Windows systems.
"""

import json
import sys
import os
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    # Try to set UTF-8 encoding for Windows console
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Fallback for older Python versions
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

    # Set console code page to UTF-8
    os.system('chcp 65001 >nul 2>&1')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from archi_mcp.server import DiagramInput


def test_json_validation():
    """Test JSON validation and parsing."""
    print("=" * 80)
    print("Testing Flower Business Diagram JSON Validation (Windows)")
    print("=" * 80)
    print()

    # Load the corrected JSON
    json_file = Path(__file__).parent / "flower_business_corrected.json"
    print(f"Loading JSON from: {json_file}")

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        print("✅ JSON file loaded successfully")
        print(f"   - Elements: {len(json_data.get('elements', []))}")
        print(f"   - Relationships: {len(json_data.get('relationships', []))}")
        print()
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        return False

    # Test DiagramInput validation
    print("Testing DiagramInput validation...")
    try:
        # Test 1: Parse from dict (Claude Desktop mode)
        print("\n1. Testing dict input (Claude Desktop mode):")
        diagram_from_dict = DiagramInput(**json_data)
        print(f"   ✅ Successfully parsed diagram from dict")
        print(f"   - Title: {diagram_from_dict.title}")
        print(f"   - Elements: {len(diagram_from_dict.elements)}")
        print(f"   - Relationships: {len(diagram_from_dict.relationships)}")

        # Test 2: Parse from JSON string (Claude Code mode)
        print("\n2. Testing JSON string input (Claude Code mode):")
        json_string = json.dumps(json_data)
        diagram_from_string = DiagramInput.model_validate(json_string)
        print(f"   ✅ Successfully parsed diagram from JSON string")
        print(f"   - Title: {diagram_from_string.title}")
        print(f"   - Elements: {len(diagram_from_string.elements)}")
        print(f"   - Relationships: {len(diagram_from_string.relationships)}")

        # Validate element types
        print("\n3. Validating element types:")
        element_types = set(elem.element_type for elem in diagram_from_dict.elements)
        print(f"   ✅ Found {len(element_types)} unique element types:")
        for elem_type in sorted(element_types):
            count = sum(1 for e in diagram_from_dict.elements if e.element_type == elem_type)
            print(f"      - {elem_type}: {count}")

        # Validate layers
        print("\n4. Validating layers:")
        layers = set(elem.layer for elem in diagram_from_dict.elements)
        print(f"   ✅ Found {len(layers)} layers:")
        for layer in sorted(layers):
            count = sum(1 for e in diagram_from_dict.elements if e.layer == layer)
            print(f"      - {layer}: {count} elements")

        # Validate relationships
        print("\n5. Validating relationships:")
        rel_types = set(rel.relationship_type for rel in diagram_from_dict.relationships)
        print(f"   ✅ Found {len(rel_types)} unique relationship types:")
        for rel_type in sorted(rel_types):
            count = sum(1 for r in diagram_from_dict.relationships if r.relationship_type == rel_type)
            print(f"      - {rel_type}: {count}")

        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED - JSON is valid and ready to use!")
        print("=" * 80)
        print()
        print("Next steps:")
        print("1. Start the MCP server: uv run python src/archi_mcp/server.py")
        print("2. Configure Claude Desktop with the MCP server")
        print("3. Use the corrected JSON in Claude Desktop to generate the diagram")
        print()

        return True

    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_common_errors():
    """Show common JSON errors and how to fix them."""
    print("\n" + "=" * 80)
    print("Common JSON Errors and Fixes")
    print("=" * 80)
    print()
    print("❌ WRONG: \"language: en\"")
    print("✅ RIGHT: \"language\": \"en\"")
    print()
    print("❌ WRONG: {}")
    print("           \"id\": \"customer\"")
    print("✅ RIGHT: {")
    print("           \"id\": \"customer\"")
    print()
    print("❌ WRONG: \"name: ustomer\"")
    print("✅ RIGHT: \"name\": \"Customer\"")
    print()
    print("❌ WRONG: \"element_type\": \"Business_Process,")
    print("✅ RIGHT: \"element_type\": \"Business_Process\",")
    print()
    print("=" * 80)


if __name__ == "__main__":
    print("\n")
    success = test_json_validation()

    if not success:
        show_common_errors()
        sys.exit(1)

    sys.exit(0)
