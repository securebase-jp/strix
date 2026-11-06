"""Minimal message catalog for localizing user-facing Strix output.

The language comes from ``STRIX_LANGUAGE`` (``en`` or ``ja``). Anything unknown
or unset falls back to English, and a key missing from a catalog falls back to
the English text, so an incomplete translation never breaks a run.
"""

from __future__ import annotations

import os
from typing import Any

from strix.i18n.catalog import CATALOGS


DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = tuple(CATALOGS)

LANGUAGE_NAMES = {"en": "English", "ja": "Japanese"}


def get_language() -> str:
    raw = (os.environ.get("STRIX_LANGUAGE") or "").strip().lower().replace("_", "-")
    code = raw.split("-")[0]
    return code if code in CATALOGS else DEFAULT_LANGUAGE


def t(key: str, **kwargs: Any) -> str:
    """Return the message for ``key`` in the active language."""
    text = CATALOGS[get_language()].get(key) or CATALOGS[DEFAULT_LANGUAGE][key]
    return text.format(**kwargs) if kwargs else text
