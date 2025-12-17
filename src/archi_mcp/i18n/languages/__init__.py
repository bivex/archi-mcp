"""Language dictionary modules for multilingual support."""

from .english import ENGLISH_DICT
from .slovak import SLOVAK_DICT
from .russian import RUSSIAN_DICT
from .ukrainian import UKRAINIAN_DICT

AVAILABLE_LANGUAGES = {
    "en": ENGLISH_DICT,
    "sk": SLOVAK_DICT,
    "ru": RUSSIAN_DICT,
    "uk": UKRAINIAN_DICT,
}

__all__ = ["ENGLISH_DICT", "SLOVAK_DICT", "RUSSIAN_DICT", "UKRAINIAN_DICT", "AVAILABLE_LANGUAGES"]