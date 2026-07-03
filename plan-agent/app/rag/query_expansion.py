from langchain_core.language_models import BaseChatModel

QUERY_EXPANSION_PROMPT = """你是一个查询改写助手。将用户输入改写为 {n} 个不同角度的搜索查询，用于从知识库中检索相关计划。

要求：
- 每个查询独立一行，不要编号
- 覆盖不同的关键词和表述方式
- 保持用户原始意图不变
- 查询应简短（不超过20字）

用户输入：{query}

改写结果（{n} 行）："""


async def expand_query(
    query: str,
    llm: BaseChatModel,
    n: int = 3,
) -> list[str]:
    """Generate multiple query variants to improve retrieval recall.

    Args:
        query: The original user query.
        llm: The LLM instance to use for rewriting.
        n: Number of query variants to generate.

    Returns:
        A list of query strings (original + variants), deduplicated.
    """
    if not query.strip():
        return []

    prompt = QUERY_EXPANSION_PROMPT.format(query=query, n=n)
    response = await llm.ainvoke(prompt)

    variants = [
        line.strip()
        for line in str(response.content).split("\n")
        if line.strip()
    ]

    seen = set()
    result: list[str] = []
    for v in variants:
        if v not in seen:
            seen.add(v)
            result.append(v)

    return result
