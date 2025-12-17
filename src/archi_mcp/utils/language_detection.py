"""Language detection utilities for ArchiMate diagrams."""

from typing import List, Set


# Slovak language indicators - common words and patterns
_SLOVAK_INDICATORS: Set[str] = {
    # Common Slovak words
    'zákazník', 'podpora', 'služba', 'proces', 'objekt', 'komponent',
    'podnikový', 'zákaznícky', 'proaktívna', 'inteligentý', 'znalostná',
    'konverzačná', 'vylepšený', 'starostlivosť', 'riešenie', 'problémov',
    'schopnosť', 'platforma', 'báza', 'profil', 'analýza', 'nálady',
    'spokojnosť', 'sledovanie', 'emócií', 'monitoruje', 'aktualizuje',
    'pristupuje', 'spúšťa', 'umožňuje', 'napájaný', 'asistovaný',
    # Slovak diacritics patterns
    'ň', 'ť', 'ž', 'č', 'š', 'ľ', 'ý', 'á', 'í', 'é', 'ó', 'ú', 'ô'
}

# Threshold for Slovak detection - minimum Slovak indicators to trigger Slovak
_SLOVAK_THRESHOLD = 3


class LanguageDetector:
    """Detects the language of ArchiMate diagram content."""

    @staticmethod
    def detect_language_from_content(diagram) -> str:
        """Automatically detect language from diagram content.

        Args:
            diagram: DiagramInput with elements and relationships

        Returns:
            Language code (e.g., "sk", "en")
        """
        all_text = LanguageDetector._collect_text_content(diagram)
        content = ' '.join(all_text)

        slovak_score = LanguageDetector._count_slovak_indicators(content)

        return "sk" if slovak_score >= _SLOVAK_THRESHOLD else "en"

    @staticmethod
    def _collect_text_content(diagram) -> List[str]:
        """Collect all text content from diagram elements and relationships."""
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

    @staticmethod
    def _count_slovak_indicators(content: str) -> int:
        """Count Slovak language indicators in the content."""
        return sum(1 for indicator in _SLOVAK_INDICATORS if indicator in content)