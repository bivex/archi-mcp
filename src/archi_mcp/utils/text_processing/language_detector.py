"""Language detection utilities."""

from typing import Set
from .extractor import TextExtractor

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
    """Detects the language of text content."""

    @staticmethod
    def detect_language_from_content(diagram) -> str:
        """Automatically detect language from diagram content.

        Args:
            diagram: DiagramInput with elements and relationships

        Returns:
            Language code (e.g., "sk", "en")
        """
        all_text = TextExtractor.collect_text_content(diagram)
        content = ' '.join(all_text)

        slovak_score = LanguageDetector._count_slovak_indicators(content)

        return "sk" if slovak_score >= _SLOVAK_THRESHOLD else "en"

    @staticmethod
    def _count_slovak_indicators(content: str) -> int:
        """Count Slovak language indicators in the content.

        Args:
            content: Text content to analyze

        Returns:
            Number of Slovak indicators found
        """
        return sum(1 for indicator in _SLOVAK_INDICATORS if indicator in content)

    @staticmethod
    def get_slovak_indicators() -> Set[str]:
        """Get the set of Slovak language indicators.

        Returns:
            Set of Slovak indicator strings
        """
        return _SLOVAK_INDICATORS.copy()

    @staticmethod
    def get_slovak_threshold() -> int:
        """Get the threshold for Slovak language detection.

        Returns:
            Minimum number of indicators to trigger Slovak detection
        """
        return _SLOVAK_THRESHOLD