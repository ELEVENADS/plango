# Agent层设计

## 技术栈
| 组件     | 技术                  | 说明                        |
|--------|---------------------|---------------------------|
| Web 框架 | FastAPI             | 高性能异步框架，自动生成 OpenAPI 文档   |
| 工作流引擎  | LangGraph 1.0+      | 构建 LLM 应用的状态图，支持条件分支、工具调用 |
| LLM 集成 | LangChain 1.0+      | 统一调用多种 LLM（OpenAI、通义千问等）  |
| 数据校验   | Pydantic v2         | 请求/响应模型定义，类型安全            |
| 配置管理   | pydantic-settings   | 从环境变量或 .env 文件加载配置        |
| 异步并发   | asyncio + Semaphore | 限制并发 LLM 请求数，避免资源耗尽       |
| Python | 3.11+               | 支持最新 LangChain/LangGraph  |
| 部署     | Docker              | 与整体微服务架构一致的容器化部署          |

## 目录数结构
```
plan-agent/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI 入口，启动服务
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py              # 依赖注入（LLM 实例、配置等）
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── generate.py      # 计划生成相关路由
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # 全局配置（模型、API Key 等）
│   │   └── logging.py           # 日志配置
│   │
│   ├── agents/                  # 智能体集合
│   │   ├── __init__.py
│   │   ├── base.py              # Agent 基类（通用接口）
│   │   ├── plan_generator/      # 计划生成 Agent
│   │   │   ├── __init__.py
│   │   │   ├── graph.py         # LangGraph 状态图定义
│   │   │   ├── prompts.py       # 提示词模板
│   │   │   └── schemas.py       # 该 Agent 专属状态模型
│   │   └── plan_review/         # 未来：计划复盘 Agent
│   │       ├── __init__.py
│   │       ├── graph.py
│   │       ├── prompts.py
│   │       └── schemas.py
│   │
│   ├── tools/                   # 可被 Agent 调用的工具
│   │   ├── __init__.py
│   │   ├── search.py            # Elasticsearch 检索工具
│   │   └── database.py          # 数据库查询工具（预留）
│   │
│   ├── models/                  # 通用数据模型（API 契约）
│   │   ├── __init__.py
│   │   ├── request.py           # 统一请求体
│   │   └── response.py          # 统一响应体
│   │
│   └── services/                # 服务层，编排 Agent 调用
│       ├── __init__.py
│       └── plan_service.py      # 计划业务逻辑
│
├── tests/                       # 单元测试
│   ├── __init__.py
│   ├── test_plan_generator.py
│   └── conftest.py
├── requirements.txt
├── Dockerfile
├── .env.example                 # 环境变量模板
└── README.md                    # Agent 层说明文档
```
## 模块职责说明
### API 层 (api/)
负责 HTTP 请求与响应的处理，参数校验，调用服务层。
使用 FastAPI 的 APIRouter 实现路由分组，支持版本化（v1/）。
deps.py 提供依赖注入，例如获取 LLM 实例、Service 实例等，便于测试和解耦。

### 核心配置 (core/)
config.py：集中管理所有配置项（LLM API Key、模型名称、温度参数、服务端口等），通过 pydantic-settings 从环境变量加载。
logging.py：统一日志格式，区分开发/生产环境日志级别。

### 智能体 (agents/)
每个 Agent 独立一个子目录，包含其专属的状态图、提示词和内部数据模型。
base.py 定义抽象基类，规定 ainvoke、stream 等通用方法，方便扩展新 Agent。
plan_generator/：当前核心 Agent，负责接收用户需求，调用 LLM 生成结构化计划。

### 工具集 (tools/)
存放可被 Agent 调用的外部工具函数，用于函数调用（Function Calling）场景。
search.py：封装 Elasticsearch 查询，用于 RAG 检索历史计划。
database.py：预留数据库查询工具，未来若 Agent 需要直接查数据可在这里实现。

### 通用模型 (models/)
定义与 Java 端对齐的 Pydantic 模型，作为 API 契约。
request.py：PlanGenerateRequest 等所有请求体。
response.py：PlanGenerateResponse 等所有响应体。

### 服务层 (services/)
编排复杂业务流程，如调用 Agent、处理结果、触发通知（通过回调或消息）。
plan_service.py：示例，调用 plan_generator Agent，并格式化返回结果。

### 测试 (tests/)
单元测试和集成测试，覆盖 Agent 逻辑、API 接口等。