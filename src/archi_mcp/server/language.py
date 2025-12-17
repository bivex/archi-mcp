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

    # Use the LanguageDetector's method directly
    return LanguageDetector.detect_language_from_content(diagram)