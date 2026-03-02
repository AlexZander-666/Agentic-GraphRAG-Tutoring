"""Pydantic 数据模型定义"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ScenarioType(str, Enum):
    """场景类型"""
    RADIOLOGY = "radiology"      # 课堂讲义
    MEDICATION = "medication"    # 实验报告
    NEWS = "news"                # 课程知识点
    FINANCE = "finance"          # 工程习题
    MEDICAL = "medical"          # 学习日志
    SALES = "sales"              # 作业批改
    CUSTOMER_SERVICE = "customer_service"  # 答疑对话
    CUSTOM = "custom"            # 自定义


class CharInterval(BaseModel):
    """字符位置区间"""
    start_pos: int = Field(..., description="起始位置")
    end_pos: int = Field(..., description="结束位置")


class ExtractionItem(BaseModel):
    """单个提取项"""
    extraction_class: str = Field(..., description="提取类别")
    extraction_text: str = Field(..., description="提取文本")
    attributes: Optional[Dict[str, Any]] = Field(default=None, description="属性")
    char_interval: Optional[CharInterval] = Field(default=None, description="字符位置")


class SegmentInfo(BaseModel):
    """段落信息（用于讲义/实验等分段场景）"""
    type: str = Field(..., description="段落类型")
    label: Optional[str] = Field(default=None, description="段落标签")
    content: str = Field(..., description="段落内容")
    intervals: List[CharInterval] = Field(default_factory=list, description="字符位置列表")
    significance: Optional[str] = Field(default=None, description="重要性")


class ExtractionRequest(BaseModel):
    """提取请求"""
    text: str = Field(..., min_length=1, max_length=100000, description="输入文本")  # 增加到 100000 以支持长文档
    scenario: ScenarioType = Field(default=ScenarioType.RADIOLOGY, description="场景类型")
    use_cache: bool = Field(default=True, description="是否使用缓存")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "叠加定理适用于线性网络，多个独立电源共同作用的响应可代数相加。",
                "scenario": "radiology",
                "use_cache": True
            }
        }


class ExtractionResponse(BaseModel):
    """提取响应"""
    success: bool = Field(..., description="是否成功")
    scenario: ScenarioType = Field(..., description="场景类型")
    segments: List[SegmentInfo] = Field(default_factory=list, description="分段结果")
    extractions: List[ExtractionItem] = Field(default_factory=list, description="提取结果")
    formatted_text: str = Field(default="", description="格式化后的文本")
    sanitized_input: str = Field(default="", description="预处理后的输入")
    from_cache: bool = Field(default=False, description="是否来自缓存")
    error: Optional[str] = Field(default=None, description="错误信息")
    processing_time: Optional[float] = Field(default=None, description="处理时间(秒)")


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str = Field(..., description="状态")
    version: str = Field(..., description="版本")
    model: str = Field(..., description="使用的模型")


class ScenarioInfo(BaseModel):
    """场景信息"""
    id: str = Field(..., description="场景ID")
    name: str = Field(..., description="场景名称")
    description: str = Field(..., description="场景描述")
    extract_classes: List[str] = Field(..., description="提取类别列表")


class SampleReport(BaseModel):
    """样本报告"""
    id: str = Field(..., description="样本ID")
    title: str = Field(..., description="标题")
    scenario: ScenarioType = Field(..., description="场景类型")
    text: str = Field(..., description="文本内容")


# =============================================================================
# PDF 解析相关模型
# =============================================================================

class PDFParseRequest(BaseModel):
    """PDF 解析请求"""
    pdf_url: str = Field(..., description="PDF 文件 URL")
    model_version: str = Field(default="vlm", description="模型版本 (vlm/pipeline)")
    extract_after_parse: bool = Field(default=True, description="解析后是否进行信息提取")
    scenario: Optional[ScenarioType] = Field(default=None, description="提取场景类型")

    class Config:
        json_schema_extra = {
            "example": {
                "pdf_url": "https://example.com/document.pdf",
                "model_version": "vlm",
                "extract_after_parse": True,
                "scenario": "news"
            }
        }


class PDFParseResponse(BaseModel):
    """PDF 解析响应"""
    success: bool = Field(..., description="是否成功")
    task_id: Optional[str] = Field(default=None, description="任务 ID")
    markdown: Optional[str] = Field(default=None, description="解析后的 Markdown 文本")
    source: str = Field(..., description="PDF 来源")
    parse_time: Optional[float] = Field(default=None, description="解析耗时(秒)")
    extractions: List[ExtractionItem] = Field(default_factory=list, description="提取结果")
    error: Optional[str] = Field(default=None, description="错误信息")


class PDFTaskStatusResponse(BaseModel):
    """PDF 任务状态响应"""
    task_id: str = Field(..., description="任务 ID")
    state: str = Field(..., description="任务状态")
    progress: Optional[Dict[str, Any]] = Field(default=None, description="进度信息")
    error: Optional[str] = Field(default=None, description="错误信息")


# =============================================================================
# 语义搜索相关模型
# =============================================================================

class SearchRequest(BaseModel):
    """语义搜索请求"""
    query: str = Field(..., min_length=1, description="搜索查询")
    top_k: int = Field(default=5, ge=1, le=20, description="返回结果数量")
    doc_id: Optional[str] = Field(default=None, description="限定文档 ID")
    chunk_type: Optional[str] = Field(default=None, description="限定片段类型")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "叠加定理 适用条件",
                "top_k": 5
            }
        }


class SearchResult(BaseModel):
    """搜索结果项"""
    score: float = Field(..., description="相关度分数")
    chunk_id: str = Field(..., description="片段 ID")
    doc_id: str = Field(..., description="文档 ID")
    doc_title: str = Field(..., description="文档标题")
    content: str = Field(..., description="内容")
    chunk_type: str = Field(..., description="片段类型")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="属性")


class SearchResponse(BaseModel):
    """语义搜索响应"""
    success: bool = Field(..., description="是否成功")
    query: str = Field(..., description="搜索查询")
    results: List[SearchResult] = Field(default_factory=list, description="搜索结果")
    total: int = Field(default=0, description="结果总数")
    error: Optional[str] = Field(default=None, description="错误信息")


# =============================================================================
# 智能问答相关模型
# =============================================================================

class QARequest(BaseModel):
    """问答请求"""
    question: str = Field(..., min_length=1, description="用户问题")
    top_k: int = Field(default=5, ge=1, le=10, description="检索数量")
    system_prompt: Optional[str] = Field(default=None, description="自定义系统提示词")
    entities: List[Dict[str, Any]] = Field(default_factory=list, description="已提取的实体列表（用于结构化展示）")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "叠加定理在什么条件下成立？",
                "top_k": 5,
                "entities": [
                    {"text": "叠加定理", "entity_type": "定理"},
                    {"text": "线性网络", "entity_type": "适用条件"}
                ]
            }
        }


class QASource(BaseModel):
    """问答来源引用"""
    doc_id: str = Field(..., description="文档 ID")
    doc_title: str = Field(..., description="文档标题")
    content_preview: str = Field(..., description="内容预览")
    score: float = Field(..., description="相关度分数")


class EntityInfo(BaseModel):
    """实体信息（用于结构化展示）"""
    text: str = Field(..., description="实体文本")
    entity_type: str = Field(..., description="实体类型")
    confidence: float = Field(default=0.9, description="置信度")
    start_pos: Optional[int] = Field(default=None, description="在答案中的起始位置")
    end_pos: Optional[int] = Field(default=None, description="在答案中的结束位置")


class QAResponse(BaseModel):
    """问答响应"""
    success: bool = Field(..., description="是否成功")
    question: str = Field(..., description="用户问题")
    answer: Optional[str] = Field(default=None, description="回答内容")
    sources: List[QASource] = Field(default_factory=list, description="引用来源")
    context_count: int = Field(default=0, description="检索到的上下文数量")
    entities: List[EntityInfo] = Field(default_factory=list, description="答案中的实体信息")
    error: Optional[str] = Field(default=None, description="错误信息")


class ChatMessage(BaseModel):
    """对话消息"""
    role: str = Field(..., description="角色 (user/assistant)")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    """对话请求"""
    messages: List[ChatMessage] = Field(..., min_length=1, description="对话历史")
    use_rag: bool = Field(default=True, description="是否使用 RAG 检索")
    top_k: int = Field(default=5, ge=1, le=10, description="检索数量")

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "user", "content": "请总结本章关于节点电压法的核心步骤"}
                ],
                "use_rag": True,
                "top_k": 5
            }
        }


class ChatResponse(BaseModel):
    """对话响应"""
    success: bool = Field(..., description="是否成功")
    answer: Optional[str] = Field(default=None, description="回答内容")
    sources: List[QASource] = Field(default_factory=list, description="引用来源")
    error: Optional[str] = Field(default=None, description="错误信息")


# =============================================================================
# 文档管理相关模型
# =============================================================================

class DocumentInfo(BaseModel):
    """文档信息"""
    doc_id: str = Field(..., description="文档 ID")
    title: str = Field(..., description="标题")
    content_preview: str = Field(..., description="内容预览")
    chunk_count: int = Field(default=0, description="片段数量")
    created_at: Optional[str] = Field(default=None, description="创建时间")


class AddDocumentRequest(BaseModel):
    """添加文档请求"""
    doc_id: Optional[str] = Field(default=None, description="文档 ID，不传则自动生成")
    title: str = Field(..., description="文档标题")
    content: str = Field(..., min_length=1, description="文档内容")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "示例文档",
                "content": "这是文档的内容...",
                "metadata": {"source": "manual", "type": "teaching_note"}
            }
        }


class KnowledgeExtractionItem(BaseModel):
    """知识提取项（用于存储到向量库）"""
    extraction_class: str = Field(..., description="提取类别（实体、关系描述、数据指标等）")
    extraction_text: str = Field(..., description="提取的文本内容")
    char_interval: Optional[CharInterval] = Field(default=None, description="原文位置")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="属性信息")


class AddExtractionsRequest(BaseModel):
    """添加知识提取结果请求"""
    doc_id: Optional[str] = Field(default=None, description="文档 ID，不传则自动生成")
    doc_title: str = Field(..., description="文档标题")
    extractions: List[KnowledgeExtractionItem] = Field(..., min_length=1, description="知识提取结果列表")

    class Config:
        json_schema_extra = {
            "example": {
                "doc_title": "电路课程知识提取",
                "extractions": [
                    {
                        "extraction_class": "概念",
                        "extraction_text": "叠加定理",
                        "char_interval": {"start_pos": 100, "end_pos": 102},
                        "attributes": {"章节": "第4章", "用途": "线性电路分析"}
                    },
                    {
                        "extraction_class": "适用条件",
                        "extraction_text": "适用于线性网络",
                        "char_interval": {"start_pos": 200, "end_pos": 215},
                        "attributes": {"关联对象": "叠加定理"}
                    }
                ]
            }
        }


class AddExtractionsResponse(BaseModel):
    """添加知识提取结果响应"""
    success: bool = Field(..., description="是否成功")
    doc_id: str = Field(..., description="文档 ID")
    chunk_count: int = Field(default=0, description="创建的向量数量")
    error: Optional[str] = Field(default=None, description="错误信息")


class AddDocumentResponse(BaseModel):
    """添加文档响应"""
    success: bool = Field(..., description="是否成功")
    doc_id: str = Field(..., description="文档 ID")
    chunk_count: int = Field(default=0, description="创建的片段数量")
    error: Optional[str] = Field(default=None, description="错误信息")


class VectorStoreStats(BaseModel):
    """向量存储统计"""
    collection_name: str = Field(..., description="集合名称")
    vectors_count: int = Field(default=0, description="向量数量")
    points_count: int = Field(default=0, description="点数量")
