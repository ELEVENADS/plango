import asyncio

from elasticsearch import Elasticsearch
from langchain_core.language_models import BaseChatModel
from langchain_openai import OpenAIEmbeddings

from app.rag.config import rag_settings
from app.rag.query_expansion import expand_query
from app.rag.retrieval import HybridRetriever


class RAGPipeline:
    """End-to-end RAG pipeline: expand query → hybrid retrieve → deduplicate → format.

    Usage::

        es = Elasticsearch(settings.elasticsearch_url)
        pipeline = RAGPipeline(es, embedding_model, llm)
        context = await pipeline.run("帮我安排明天的学习计划", user_id=100)
    """

    def __init__(
        self,
        es: Elasticsearch,
        embedding_model: OpenAIEmbeddings,
        llm: BaseChatModel,
        index_name: str | None = None,
    ) -> None:
        self.retriever = HybridRetriever(es, embedding_model, index_name)
        self.llm = llm

    async def run(
        self,
        query: str,
        user_id: int,
        expand: bool | None = None,
        top_k: int | None = None,
    ) -> str:
        """Execute the full RAG pipeline and return formatted context text.

        Args:
            query: The user's natural language query.
            user_id: User ID for data isolation.
            expand: Whether to use query expansion. Defaults to config setting.
            top_k: Number of final results. Defaults to config setting.

        Returns:
            Formatted context string, or empty string if nothing retrieved.
        """
        expand = expand if expand is not None else rag_settings.query_expansion_enabled

        if expand:
            queries = await expand_query(query, self.llm, rag_settings.query_expansion_variants)
            if not queries:
                queries = [query]
        else:
            queries = [query]

        tasks = [self.retriever.retrieve(q, user_id) for q in queries]
        result_sets = await asyncio.gather(*tasks)

        merged: dict[str, dict] = {}
        for results in result_sets:
            for doc in results:
                doc_id = doc["id"]
                if doc_id not in merged:
                    merged[doc_id] = doc
                else:
                    merged[doc_id]["_combined_score"] = max(
                        merged[doc_id].get("_combined_score", 0),
                        doc.get("_combined_score", 0),
                    )

        ranked = sorted(
            merged.values(),
            key=lambda d: d.get("_combined_score", 0),
            reverse=True,
        )

        top_k = top_k or rag_settings.retrieval_top_k
        return self._format_context(ranked[:top_k])

    @staticmethod
    def _format_context(docs: list[dict]) -> str:
        if not docs:
            return ""

        lines = []
        for doc in docs:
            parts = [f"标题：{doc.get('title', '')}"]
            desc = doc.get("description")
            if desc:
                parts.append(f"描述：{desc}")
            parts.append(
                f"日期：{doc.get('plan_date', '')}  "
                f"{doc.get('start_time', '')}~{doc.get('end_time', '')}"
            )
            tags = doc.get("tags")
            if tags:
                parts.append(f"标签：{tags}")
            lines.append(" | ".join(parts))

        return "\n".join(lines)
