"""Embedding provider 解析与回退。"""

import logging
from typing import Tuple

from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)


class EmbeddingInitError(ValueError):
    """Embedding 初始化失败。"""


def _short_error_message(error: Exception, max_length: int = 240) -> str:
    message = str(error).replace("\n", " ").strip()
    if len(message) <= max_length:
        return message
    return f"{message[:max_length]}..."


def build_openai_embeddings(
    primary_model: str,
    primary_api_key: str,
    primary_base_url: str,
    fallback_api_key: str = "",
    fallback_base_url: str = "https://api.siliconflow.cn/v1",
    fallback_model: str = "BAAI/bge-m3",
    probe_text: str = "embedding healthcheck",
) -> Tuple[OpenAIEmbeddings, str, str]:
    """
    构建 Embedding 客户端，支持主供应商失败后回退。

    返回: (embeddings, active_model, active_base_url)
    """
    candidates = []
    if primary_api_key:
        candidates.append(
            ("primary", primary_model, primary_api_key, primary_base_url)
        )

    if fallback_api_key:
        duplicate = (
            primary_api_key
            and fallback_api_key == primary_api_key
            and fallback_base_url == primary_base_url
            and fallback_model == primary_model
        )
        if not duplicate:
            candidates.append(
                ("siliconflow", fallback_model, fallback_api_key, fallback_base_url)
            )

    if not candidates:
        raise EmbeddingInitError(
            "未配置可用 Embedding Key，请设置 DASHSCOPE_API_KEY 或 SILICONFLOW_API_KEY。"
        )

    errors = []
    for provider, model, api_key, base_url in candidates:
        try:
            embeddings = OpenAIEmbeddings(
                model=model,
                api_key=api_key,
                base_url=base_url,
                check_embedding_ctx_length=False,
                chunk_size=10,
            )
            # 通过一次最小探测，提前暴露无效 key 或模型配置错误。
            embeddings.embed_query(probe_text)
            logger.info("Embedding provider 已启用: %s (%s)", provider, model)
            return embeddings, model, base_url
        except Exception as exc:
            short_error = _short_error_message(exc)
            logger.warning(
                "Embedding provider 初始化失败: %s (%s) -> %s",
                provider,
                model,
                short_error,
            )
            errors.append(f"{provider}: {short_error}")

    raise EmbeddingInitError(
        "Embedding 初始化失败，请检查 DASHSCOPE_API_KEY/SILICONFLOW_API_KEY 与模型配置。"
        + (" 上游错误: " + " | ".join(errors) if errors else "")
    )
