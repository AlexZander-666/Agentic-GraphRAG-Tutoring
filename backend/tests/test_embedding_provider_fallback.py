import pytest

from app.utils.embedding_provider import EmbeddingInitError, build_openai_embeddings


class _FakeEmbeddings:
    def __init__(self, model, api_key, base_url, **kwargs):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

    def embed_query(self, text):
        if "dashscope.aliyuncs.com" in self.base_url:
            raise Exception(
                "Error code: 401 - {'error': {'code': 'invalid_api_key'}}"
            )
        return [0.1, 0.2, 0.3]


def test_falls_back_to_siliconflow_when_dashscope_auth_fails(monkeypatch):
    monkeypatch.setattr(
        "app.utils.embedding_provider.OpenAIEmbeddings",
        _FakeEmbeddings,
    )

    _, model, base_url = build_openai_embeddings(
        primary_model="text-embedding-v4",
        primary_api_key="bad-dashscope-key",
        primary_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        fallback_api_key="valid-siliconflow-key",
        fallback_base_url="https://api.siliconflow.cn/v1",
        fallback_model="BAAI/bge-m3",
    )

    assert model == "BAAI/bge-m3"
    assert base_url == "https://api.siliconflow.cn/v1"


def test_raises_clear_error_when_no_embedding_key():
    with pytest.raises(EmbeddingInitError) as exc:
        build_openai_embeddings(
            primary_model="text-embedding-v4",
            primary_api_key="",
            primary_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            fallback_api_key="",
            fallback_base_url="https://api.siliconflow.cn/v1",
            fallback_model="BAAI/bge-m3",
        )

    assert "DASHSCOPE_API_KEY 或 SILICONFLOW_API_KEY" in str(exc.value)
