"""Markdown documentation generation for ArchiMate diagrams."""

from typing import List
from ..i18n import ArchiMateTranslator
from ..archimate import ArchiMateGenerator


def _add_markdown_header(md_content: list, title: str, description: str, png_filename: str, translator):
    """Add header section to markdown content."""
    md_content.append(f"# {title}")
    md_content.append("")

    if description:
        md_content.append(f"**Description:** {description}")
        md_content.append("")

    md_content.append(f"![{title}]({png_filename})")
    md_content.append("")


def _add_markdown_overview(md_content: list, generator, translator):
    """Add overview section with basic statistics."""
    elements_count = len(generator.elements)
    relationships_count = len(generator.relationships)

    md_content.append("## Overview")
    md_content.append("")

    overview_data = [
        ("Total Elements", elements_count),
        ("Total Relationships", relationships_count),
    ]

    # Count elements by layer
    layer_counts = {}
    for element in generator.elements.values():
        layer = element.layer.value if hasattr(element.layer, 'value') else str(element.layer)
        layer_counts[layer] = layer_counts.get(layer, 0) + 1

    for layer, count in sorted(layer_counts.items()):
        overview_data.append((f"{layer} Elements", count))

    # Create table
    md_content.append("| Metric | Count |")
    md_content.append("|--------|-------|")
    for metric, count in overview_data:
        md_content.append(f"| {metric} | {count} |")
    md_content.append("")


def _add_elements_by_layer(md_content: list, generator, translator):
    """Add detailed elements section organized by layer."""
    md_content.append("## Elements by Layer")
    md_content.append("")

    # Group elements by layer
    layers = {}
    for element in generator.elements.values():
        layer = element.layer.value if hasattr(element.layer, 'value') else str(element.layer)
        if layer not in layers:
            layers[layer] = []
        layers[layer].append(element)

    for layer_name in sorted(layers.keys()):
        md_content.append(f"### {layer_name} Layer")
        md_content.append("")

        elements = layers[layer_name]

        if elements:
            md_content.append("| Element | Type | Description |")
            md_content.append("|---------|------|-------------|")

            for element in sorted(elements, key=lambda x: x.name):
                desc = element.description[:50] + "..." if element.description and len(element.description) > 50 else (element.description or "")
                md_content.append(f"| {element.name} | {element.element_type} | {desc} |")

        md_content.append("")


def _add_relationships_section(md_content: list, generator, translator):
    """Add relationships section."""
    md_content.append("## Relationships")
    md_content.append("")

    if generator.relationships:
        md_content.append("| Source | Relationship | Target |")
        md_content.append("|--------|--------------|--------|")

        for rel in generator.relationships:
            source_name = generator.elements[rel.source_id].name if rel.source_id in generator.elements else rel.source_id
            target_name = generator.elements[rel.target_id].name if rel.target_id in generator.elements else rel.target_id
            rel_type = rel.relationship_type.value if hasattr(rel.relationship_type, 'value') else str(rel.relationship_type)

            md_content.append(f"| {source_name} | {rel_type} | {target_name} |")

    md_content.append("")


def _add_architecture_insights(md_content: list, generator, translator):
    """Add architecture insights and recommendations."""
    md_content.append("## Architecture Insights")
    md_content.append("")

    insights = []

    # Count different relationship types
    rel_types = {}
    for rel in generator.relationships:
        rel_type = rel.relationship_type.value if hasattr(rel.relationship_type, 'value') else str(rel.relationship_type)
        rel_types[rel_type] = rel_types.get(rel_type, 0) + 1

    if rel_types:
        insights.append("### Relationship Analysis")
        insights.append("")
        for rel_type, count in sorted(rel_types.items(), key=lambda x: x[1], reverse=True):
            insights.append(f"- **{rel_type}**: {count} relationship{'s' if count != 1 else ''}")

    # Element connectivity analysis
    element_connections = {}
    for rel in generator.relationships:
        for elem_id in [rel.source_id, rel.target_id]:
            element_connections[elem_id] = element_connections.get(elem_id, 0) + 1

    if element_connections:
        most_connected = sorted(element_connections.items(), key=lambda x: x[1], reverse=True)[:5]
        insights.append("")
        insights.append("### Most Connected Elements")
        insights.append("")
        for elem_id, connections in most_connected:
            if elem_id in generator.elements:
                elem_name = generator.elements[elem_id].name
                insights.append(f"- **{elem_name}**: {connections} connection{'s' if connections != 1 else ''}")

    if insights:
        md_content.extend(insights)
    else:
        md_content.append("No specific insights available for this architecture.")

    md_content.append("")


def _add_markdown_footer(md_content: list, translator):
    """Add footer with generation information."""
    md_content.append("---")
    md_content.append("")
    md_content.append("*Generated by ArchiMate MCP Server*")
    md_content.append("")


def generate_architecture_markdown(generator, title: str, description: str, png_filename: str = "diagram.png") -> str:
    """Generate comprehensive markdown documentation for an ArchiMate diagram."""
    md_content = []

    # Get translator (default to English if none provided)
    translator = generator.translator if hasattr(generator, 'translator') and generator.translator else ArchiMateTranslator("en")

    # Add all sections
    _add_markdown_header(md_content, title, description, png_filename, translator)
    _add_markdown_overview(md_content, generator, translator)
    _add_elements_by_layer(md_content, generator, translator)
    _add_relationships_section(md_content, generator, translator)
    _add_architecture_insights(md_content, generator, translator)
    _add_markdown_footer(md_content, translator)

    return "\n".join(md_content)


def _generate_detailed_description(generator, title: str, translator=None) -> str:
    """Generate detailed description of the architecture."""
    if not translator:
        translator = ArchiMateTranslator("en")

    elements_count = len(generator.elements)
    relationships_count = len(generator.relationships)

    description = f"This {title} contains {elements_count} elements and {relationships_count} relationships across the ArchiMate framework."

    # Add layer breakdown
    layer_counts = {}
    for element in generator.elements.values():
        layer = element.layer.value if hasattr(element.layer, 'value') else str(element.layer)
        layer_counts[layer] = layer_counts.get(layer, 0) + 1

    if layer_counts:
        layer_desc = []
        for layer, count in sorted(layer_counts.items()):
            layer_desc.append(f"{count} {layer.lower()} elements")
        description += f" It includes {', '.join(layer_desc)}."

    return description