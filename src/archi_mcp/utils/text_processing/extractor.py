# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:26
# Last Updated: 2025-12-18T11:40:26
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Text extraction utilities for diagram content."""

from typing import List


class TextExtractor:
    """Utility class for extracting text content from diagrams."""

    @staticmethod
    def collect_text_content(diagram) -> List[str]:
        """Collect all text content from diagram elements and relationships.

        Args:
            diagram: DiagramInput with elements and relationships

        Returns:
            List of text content strings
        """
        all_text = []

        all_text.extend(TextExtractor._extract_text_from_elements(diagram.elements))
        all_text.extend(TextExtractor._extract_text_from_relationships(diagram.relationships))
        all_text.extend(TextExtractor._extract_text_from_diagram_metadata(diagram))

        return all_text


    @staticmethod
    def _extract_text_from_elements(elements) -> List[str]:
        """Extract text content from diagram elements."""
        text_content = []
        for element in elements:
            if element.name:
                text_content.append(element.name.lower())
            if element.description:
                text_content.append(element.description.lower())
        return text_content

    @staticmethod
    def _extract_text_from_relationships(relationships) -> List[str]:
        """Extract text content from diagram relationships."""
        text_content = []
        for rel in relationships:
            if rel.label:
                text_content.append(rel.label.lower())
            if rel.description:
                text_content.append(rel.description.lower())
        return text_content

    @staticmethod
    def _extract_text_from_diagram_metadata(diagram) -> List[str]:
        """Extract text content from diagram title and description."""
        text_content = []
        if diagram.title:
            text_content.append(diagram.title.lower())
        if diagram.description:
            text_content.append(diagram.description.lower())
        return text_content