from unittest.mock import AsyncMock, MagicMock

import pytest

from app.rag.query_expansion import expand_query


class TestExpandQuery:
    @pytest.mark.asyncio
    async def test_returns_deduplicated_variants(self, mock_llm) -> None:
        variants = await expand_query("给我安排今天的学习计划", mock_llm, n=3)
        assert len(variants) == 3
        assert all(isinstance(v, str) and len(v) > 0 for v in variants)

    @pytest.mark.asyncio
    async def test_deduplicates_duplicates(self) -> None:
        llm = MagicMock()
        response = MagicMock()
        response.content = "学习计划\n学习计划\n日程安排"
        llm.ainvoke = AsyncMock(return_value=response)

        variants = await expand_query("test query", llm, n=3)
        assert len(variants) == 2  # duplicate removed

    @pytest.mark.asyncio
    async def test_empty_query_returns_empty(self, mock_llm) -> None:
        variants = await expand_query("", mock_llm)
        assert variants == []

    @pytest.mark.asyncio
    async def test_empty_lines_filtered(self) -> None:
        llm = MagicMock()
        response = MagicMock()
        response.content = "学习计划\n  \nJava学习\n"
        llm.ainvoke = AsyncMock(return_value=response)

        variants = await expand_query("test", llm, n=3)
        assert len(variants) == 2
        assert "学习计划" in variants
        assert "Java学习" in variants
