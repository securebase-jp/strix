import pytest

from strix.agents.prompt import render_system_prompt
from strix.i18n import SUPPORTED_LANGUAGES, get_language, t
from strix.i18n.catalog import CATALOGS
from strix.report.writer import render_vulnerability_md


REPORT = {
    "id": "v1",
    "title": "SQLi",
    "severity": "high",
    "description": "d",
    "remediation_steps": "fix",
    "code_locations": [{"file": "a.py", "start_line": 1, "end_line": 3}],
}


def test_catalog_keys_match():
    for lang in SUPPORTED_LANGUAGES:
        assert CATALOGS[lang].keys() == CATALOGS["en"].keys()


def test_language_resolution(monkeypatch):
    monkeypatch.delenv("STRIX_LANGUAGE", raising=False)
    assert get_language() == "en"
    for value, expected in [("ja", "ja"), ("ja_JP", "ja"), ("JA-jp", "ja"), ("fr", "en")]:
        monkeypatch.setenv("STRIX_LANGUAGE", value)
        assert get_language() == expected


def test_report_default_is_english(monkeypatch):
    monkeypatch.delenv("STRIX_LANGUAGE", raising=False)
    md = render_vulnerability_md(REPORT)
    assert "## Description" in md
    assert "**Severity:** HIGH" in md
    assert "(lines 1-3)" in md


def test_report_japanese(monkeypatch):
    monkeypatch.setenv("STRIX_LANGUAGE", "ja")
    md = render_vulnerability_md(REPORT)
    assert "## 概要" in md
    assert "## 対策" in md
    assert "**重大度:** HIGH" in md
    assert "1〜3行目" in md
    assert t("report.title") == "セキュリティ侵入テストレポート"


@pytest.mark.parametrize(("lang", "present"), [("ja", True), ("en", False)])
def test_prompt_language_directive(monkeypatch, lang, present):
    monkeypatch.setenv("STRIX_LANGUAGE", lang)
    prompt = render_system_prompt()
    assert ("OUTPUT LANGUAGE:" in prompt) is present


def test_cli_completion_labels(monkeypatch):
    monkeypatch.setenv("STRIX_LANGUAGE", "ja")
    assert t("cli.targets_n", n=3) == "3 件の対象"
    monkeypatch.delenv("STRIX_LANGUAGE")
    assert t("cli.targets_n", n=3) == "3 targets"
    assert t("cli.completed") == "Penetration test completed"
