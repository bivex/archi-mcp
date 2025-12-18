# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18 11:23
# Last Updated: 2025-12-18 11:23
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

        # Add element names and descriptions
        for element in diagram.elements:
            if element.name:
                all_text.append(element.name.lower())
            if element.description:
                all_text.append(element.description.lower())

        # Add relationship labels and descriptions
        for rel in diagram.relationships:
            if rel.label:
                all_text.append(rel.label.lower())
            if rel.description:
                all_text.append(rel.description.lower())

        # Add title and description
        if diagram.title:
            all_text.append(diagram.title.lower())
        if diagram.description:
            all_text.append(diagram.description.lower())

        return all_text