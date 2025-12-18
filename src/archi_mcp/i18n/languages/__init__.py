# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18 11:24
# Last Updated: 2025-12-18 11:24
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

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