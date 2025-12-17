"""Language detection and translation utilities for the ArchiMate MCP server."""

from ..i18n import ArchiMateTranslator
from .models import DiagramInput


def translate_relationship_labels(diagram, translator: ArchiMateTranslator) -> None:
    """Override custom relationship labels with translated versions if non-English language detected.

    Args:
        diagram: DiagramInput to modify
        translator: Translator to use for relationship type translations
    """
    if translator.get_current_language() == "en":
        return  # Keep original labels for English

    # For non-English languages, use translated relationship types only if no custom label exists
    for rel in diagram.relationships:
        if rel.relationship_type:
            # Only override if no custom label is provided by client
            if not rel.label:
                # Get translated relationship type as fallback
                translated_label = translator.translate_relationship(rel.relationship_type)
                rel.label = translated_label
            # If custom label exists, keep it (client knows best)


def detect_language_from_content(diagram: DiagramInput) -> str:
    """Detect language from diagram content (titles, descriptions, element names).

    Args:
        diagram: DiagramInput to analyze

    Returns:
        str: Detected language code ('en', 'sk', 'ru', 'uk')
    """
    from ..utils.language_detection import LanguageDetector

    # Collect text content from diagram
    text_content = []

    # Add title and description
    if diagram.title:
        text_content.append(diagram.title)
    if diagram.description:
        text_content.append(diagram.description)

    # Add element names and descriptions
    for element in diagram.elements:
        text_content.append(element.name)
        if element.description:
            text_content.append(element.description)

    # Add relationship descriptions and labels
    for rel in diagram.relationships:
        if rel.description:
            text_content.append(rel.description)
        if rel.label:
            text_content.append(rel.label)

    # Join all content
    full_text = " ".join(text_content)

    if not full_text.strip():
        return "en"  # Default to English if no content

    # Use language detector
    detector = LanguageDetector()
    detected_lang = detector.detect_language(full_text)

    return detected_lang