# 基于 LangChain + Agentic-GraphRAG + 知识图谱的 AI 智能导学系统

> 面向课程学习场景的 AI 导学平台：文档解析 -> 知识提取 -> 图谱构建 -> 可溯源问答

本仓库从工程实现角度落地了参赛方案《[基于LangChain+Agentic-GraphRAG+知识图谱的AI智能导学系统](./基于LangChain+Agentic-GraphRAG+知识图谱的AI智能导学系统.md)》，重点提供可运行的前后端系统与 API。

## 项目简介

系统围绕教学导学场景构建了完整闭环：

1. 文档接入：支持示例文本、粘贴文本、PDF 上传解析（MinerU）。
2. 信息提取：基于 LangExtract + 场景模板提取教学结构化知识。
3. 知识组织：将文本与提取结果写入向量库（默认 ChromaDB）。
4. 智能问答：基于 LangChain + RAG 生成答案，返回引用证据与溯源信息。
5. 图谱呈现：前端可视化知识关系，辅助学生理解知识点关联。

## 当前实现能力

### 1) 前端（React + TypeScript + Vite）

- 支持两种使用模式：默认模式（直接问答）与交互式模式（4 步导学流程）。
- 文档输入支持：本地 PDF 上传解析、粘贴长文本、示例文档快速体验。
- 智能问答支持：流式输出（SSE）、引用来源卡片展示、原文高亮与实体匹配展示。

### 2) 后端（FastAPI）

- 基础提取 API：健康检查、场景列表、场景样本、结构化提取、缓存管理。
- RAG API：PDF 解析（URL / 上传文件）、文档入库、提取结果入库、语义搜索、问答、流式问答、多轮对话。
- 向量存储：默认 `ChromaDB`（本地持久化），可切换 `Qdrant`。
- LLM / Embedding：LLM 支持 `DeepSeek` 与 `SiliconFlow`；Embedding 支持 `DashScope` 并可回退 `SiliconFlow`。

## 教学场景映射（已内置 7 类）

为兼容历史接口，场景 `id` 与教学语义映射如下：

| 场景 ID | 教学场景 | 典型提取字段 |
| --- | --- | --- |
| `radiology` | 课堂讲义 | 章节、核心定义、推导步骤、注意事项 |
| `medication` | 实验报告 | 实验目的、实验条件、实验步骤、误差分析 |
| `news` | 课程知识点 | 概念、定理、公式、适用条件 |
| `finance` | 工程习题 | 已知条件、目标、约束条件、结论 |
| `medical` | 学习日志 | 错误归因、纠正策略、掌握度变化 |
| `sales` | 作业批改 | 得分点、失分点、反馈建议 |
| `customer_service` | 答疑对话 | 学生问题、解题思路、后续行动 |

## 架构概览

```text
Frontend (React/Vite)
  └─ 导学流程与可视化（提取、图谱、问答、溯源）
        │
        ▼
Backend API (FastAPI)
  ├─ /api/extract                文本结构化提取
  └─ /api/rag/*                  PDF、检索、问答、知识库管理
        │
        ├─ LangExtract            场景化知识提取
        ├─ MinerU                 PDF 解析
        ├─ Vector Store           ChromaDB / Qdrant
        └─ LangChain + LLM        RAG 问答（含流式）
```

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- npm 9+

### 1) 后端启动

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt

# 环境变量
# Windows:
copy .env.example .env
# macOS/Linux:
# cp .env.example .env

uvicorn app.main:app --reload --port 8001
```

后端地址：`http://localhost:8001`  
API 文档：`http://localhost:8001/docs`

### 2) 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端地址：`http://localhost:13001`

### 3) 脚本启动（可选）

- Windows：`start.bat`
- Linux/macOS（Conda 流程）：先 `./setup.sh` 再 `./start.sh`

## 环境变量说明（backend/.env）

最小可运行建议：

- LLM 至少配置一个：`DEEPSEEK_API_KEY` 或 `SILICONFLOW_API_KEY`
- Embedding 至少配置一个：`DASHSCOPE_API_KEY` 或 `SILICONFLOW_API_KEY`
- 若使用 PDF 解析，需配置：`MINERU_API_KEY`

常用配置项：

| 变量名 | 说明 | 示例 |
| --- | --- | --- |
| `DEEPSEEK_API_KEY` | DeepSeek 文本模型 Key | `sk-...` |
| `SILICONFLOW_API_KEY` | SiliconFlow Key（可作为 LLM/Embedding 回退） | `sk-...` |
| `DASHSCOPE_API_KEY` | DashScope Embedding Key | `sk-...` |
| `MINERU_API_KEY` | MinerU PDF 解析 Key | `...` |
| `VECTOR_STORE_BACKEND` | 向量库后端（`chroma`/`qdrant`） | `chroma` |
| `CHROMA_PERSIST_DIR` | Chroma 持久化目录 | `./chroma_db` |
| `QDRANT_URL` | Qdrant 地址（可选） | `http://localhost:6333` |
| `CORS_ORIGINS` | CORS 白名单（逗号分隔） | `http://localhost:13001` |

## 主要 API 概览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `GET` | `/api/health` | 健康检查 |
| `GET` | `/api/scenarios` | 获取场景列表 |
| `POST` | `/api/extract` | 文本结构化提取 |
| `POST` | `/api/rag/pdf/upload` | 上传并解析 PDF |
| `POST` | `/api/rag/search` | 语义搜索 |
| `POST` | `/api/rag/qa` | 问答 |
| `POST` | `/api/rag/qa/stream` | 流式问答（SSE） |
| `POST` | `/api/rag/extractions` | 提取结果写入知识库 |
| `GET` | `/api/rag/stats` | 知识库统计 |

## 项目结构

```text
.
├── backend
│   ├── app
│   │   ├── api/                # routes.py + rag_routes.py
│   │   ├── core/               # extractor.py
│   │   ├── models/             # schemas.py
│   │   ├── scenarios/          # 7 类教学场景定义
│   │   ├── services/           # pdf_parser / qa_agent / vector_store
│   │   └── utils/              # cache / sanitize / embedding_provider
│   └── tests/                  # pytest 测试
├── frontend
│   └── src
│       ├── components/steps/   # 四步导学界面
│       ├── context/            # 提取上下文
│       └── services/api.ts     # 前端 API 封装
├── docs
│   └── scenarios_demo.md
└── README.md
```

## 测试与构建

### 后端测试

```bash
cd backend
pytest -q
```

### 前端构建

```bash
cd frontend
npm run build
```

## 当前注意事项

- `docker-compose.yml` 已定义前后端服务，但当前仓库缺少 `frontend/Dockerfile`。如需一键容器化，请先补齐该文件后再执行 `docker compose up --build`。
- 问答质量依赖知识库内容与向量化质量，建议先完成“提取并入库”再进行问答。

## 路线图（下一步）

- 增强 Agentic 检索策略（问题分类 -> 检索策略动态选择）。
- 优化知识图谱关系抽取精度与自动化构建能力。
- 增加个性化学习路径推荐与学习轨迹分析。
- 增加本地模型与多模态内容支持（图像/公式版面）。
