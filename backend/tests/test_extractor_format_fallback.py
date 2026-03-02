from types import SimpleNamespace

import pytest

import app.core.extractor as extractor_module
from app.config import Settings
from app.core.extractor import Extractor


def _build_settings() -> Settings:
    return Settings(cache_enabled=False)


def test_perform_extraction_retries_without_wrapper_when_extractions_key_missing(
    monkeypatch: pytest.MonkeyPatch,
):
    extractor = Extractor(_build_settings())
    monkeypatch.setattr(extractor, "_get_model", lambda: object())

    calls = []

    def fake_extract(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            raise ValueError("Content must contain an 'extractions' key.")
        return SimpleNamespace(extractions=[])

    monkeypatch.setattr(extractor_module.lx, "extract", fake_extract)

    result = extractor._perform_extraction(
        text="demo text",
        prompt="demo prompt",
        examples=[],
    )

    assert result.extractions == []
    assert len(calls) == 2
    assert calls[0].get("resolver_params") is None
    assert calls[1]["resolver_params"] == {"require_extractions_key": False}


def test_perform_extraction_does_not_retry_for_unrelated_errors(
    monkeypatch: pytest.MonkeyPatch,
):
    extractor = Extractor(_build_settings())
    monkeypatch.setattr(extractor, "_get_model", lambda: object())

    def fake_extract(**kwargs):
        raise RuntimeError("upstream unavailable")

    monkeypatch.setattr(extractor_module.lx, "extract", fake_extract)

    with pytest.raises(RuntimeError, match="upstream unavailable"):
        extractor._perform_extraction(
            text="demo text",
            prompt="demo prompt",
            examples=[],
        )
