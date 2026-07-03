from langchain_core.tools import tool

from app.rag.pipeline import RAGPipeline


# Populated lazily — call init_rag_tool() before first use.
_pipeline: RAGPipeline | None = None


def init_rag_tool(pipeline: RAGPipeline) -> None:
    """Inject a RAGPipeline instance for the rag_search tool."""
    global _pipeline
    _pipeline = pipeline


@tool
async def rag_search(query: str, user_id: int) -> str:
    """从知识库中检索与用户查询语义相关的历史计划和参考资料。

    当需要了解用户的历史计划、偏好、或获取与当前规划相关的上下文时调用此工具。
    返回的是格式化的相关文档内容，可直接作为 LLM 生成的参考上下文。

    Args:
        query: 用户的查询或规划意图，用于语义匹配。
        user_id: 用户 ID，用于隔离不同用户的知识库数据。

    Returns:
        格式化的相关文档文本，每条包含标题、描述、日期等信息。
    """
    if _pipeline is None:
        return ""
    return await _pipeline.run(query, user_id)
