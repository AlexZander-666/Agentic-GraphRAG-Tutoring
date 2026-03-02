from app.config import Settings


def _clear_llm_env(monkeypatch):
    keys = [
        "SILICONFLOW_API_KEY",
        "SILICONFLOW_API_BASE",
        "SILICONFLOW_TEXT_MODEL",
        "DEEPSEEK_API_KEY",
        "DEEPSEEK_BASE_URL",
        "DEFAULT_MODEL",
    ]
    for key in keys:
        monkeypatch.delenv(key, raising=False)


def test_prefers_siliconflow_when_configured(monkeypatch):
    _clear_llm_env(monkeypatch)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "deepseek-key")
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    monkeypatch.setenv("DEFAULT_MODEL", "deepseek-chat")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "siliconflow-key")
    monkeypatch.setenv("SILICONFLOW_API_BASE", "https://api.siliconflow.cn/v1")
    monkeypatch.setenv("SILICONFLOW_TEXT_MODEL", "deepseek-ai/DeepSeek-V3.2")

    settings = Settings(_env_file=None)

    assert settings.llm_api_key == "siliconflow-key"
    assert settings.llm_base_url == "https://api.siliconflow.cn/v1"
    assert settings.llm_text_model == "deepseek-ai/DeepSeek-V3.2"


def test_falls_back_to_deepseek_when_siliconflow_missing(monkeypatch):
    _clear_llm_env(monkeypatch)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "deepseek-key")
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    monkeypatch.setenv("DEFAULT_MODEL", "deepseek-chat")

    settings = Settings(_env_file=None)

    assert settings.llm_api_key == "deepseek-key"
    assert settings.llm_base_url == "https://api.deepseek.com"
    assert settings.llm_text_model == "deepseek-chat"
