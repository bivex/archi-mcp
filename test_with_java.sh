#!/bin/bash

# Script to run tests with Java available in background
# This ensures PlantUML validation works properly

set -e

echo "🚀 Starting ArchiMate MCP tests with Java support..."
echo "=================================================="

# Ensure Java is available
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"

# Verify Java is working
echo "📋 Checking Java installation..."
if ! java -version 2>&1 | grep -q "openjdk"; then
    echo "❌ Java not found or not working properly"
    echo "💡 Install OpenJDK: brew install openjdk"
    echo "💡 Or add to PATH: export PATH=\"/opt/homebrew/opt/openjdk/bin:\$PATH\""
    exit 1
fi

echo "✅ Java is available:"
java -version

echo ""
echo "🧪 Running pytest with Java support..."
echo "====================================="

# Run tests with Java available
# Use a subset of tests that actually need PlantUML/Java
pytest \
    tests/test_load_from_file.py \
    tests/test_relationships.py::TestArchiMateRelationship::test_relationship_plantuml_generation \
    tests/test_relationships.py::TestArchiMateRelationship::test_relationship_plantuml_with_direction \
    tests/test_validation_mandatory.py \
    -v \
    --tb=short \
    --durations=10 \
    --maxfail=5

echo ""
echo "🎉 Test run completed!"
echo "📊 Check coverage report: open htmlcov/index.html"