from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import RemoveMessage

from app.agents.base import BaseAgent
from app.agents.plan_generator.prompts import MEMORY_SUMMARIZE_PROMPT, SYSTEM_PROMPT
from app.agents.plan_generator.schemas import (
    PlanGeneratorState,
    StructuredPlanOutput,
)
from app.api.deps import get_llm
from app.tools.search import rag_search

MEMORY_THRESHOLD = 12
KEEP_RECENT = 6

class PlanGenerateAgent(BaseAgent):
    """Conversational plan generation agent with RAG and memory compression."""

    def __init__(self) -> None:
        from app.api.deps import get_rag_pipeline

        get_rag_pipeline()  # ensure RAG tool is wired before use
        self.llm = get_llm()
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(PlanGeneratorState)
        builder.add_node("rag_retrieve", self._rag_retrieve)
        builder.add_node("summarize_memory", self._summarize_memory)
        builder.add_node("generate", self._generate)

        builder.set_entry_point("rag_retrieve")
        builder.add_conditional_edges(
            "rag_retrieve",
            self._should_summarize,
            {"summarize": "summarize_memory", "skip": "generate"},
        )
        builder.add_edge("summarize_memory", "generate")
        builder.add_edge("generate", END)
        return builder.compile()

    # ── rag_retrieve ──────────────────────────────────────────────

    async def _rag_retrieve(self, state: PlanGeneratorState) -> dict:
        messages = state["messages"]
        user_id = state["user_id"]

        query = ""
        for m in reversed(messages):
            if isinstance(m, HumanMessage) and m.content:
                query = str(m.content)
                break

        if not query:
            return {"rag_context": ""}

        context = await rag_search.ainvoke({"query": query, "user_id": user_id})
        return {"rag_context": context}

    # ── conditional edge ──────────────────────────────────────────

    def _should_summarize(self, state: PlanGeneratorState) -> str:
        if len(state["messages"]) > MEMORY_THRESHOLD:
            return "summarize"
        return "skip"

    # ── summarize_memory ──────────────────────────────────────────

    async def _summarize_memory(self, state: PlanGeneratorState) -> dict:
        messages = state["messages"]
        old = messages[:-KEEP_RECENT]
        recent = messages[-KEEP_RECENT:]

        conversation_text = "\n".join(
            f"{'用户' if isinstance(m, HumanMessage) else '助手'}: {m.content}"
            for m in old
            if isinstance(m, (HumanMessage, AIMessage))
        )

        prompt = MEMORY_SUMMARIZE_PROMPT.format(conversation=conversation_text)
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        summary = response.content

        deletes = [RemoveMessage(id=m.id) for m in old]

        existing_summary = state.get("memory_summary", "")
        merged_summary = (
            f"{existing_summary}\n---\n{summary}"
            if existing_summary
            else summary
        )

        return {
            "messages": deletes,
            "memory_summary": merged_summary,
        }

    # ── generate ──────────────────────────────────────────────────

    async def _generate(self, state: PlanGeneratorState) -> dict:
        system_text = SYSTEM_PROMPT

        if state.get("rag_context"):
            system_text += (
                "\n\n## 知识库上下文（与当前对话相关的历史计划）\n"
                f"{state['rag_context']}"
            )

        if state.get("memory_summary"):
            system_text += (
                "\n\n## 历史对话摘要\n"
                f"{state['memory_summary']}"
            )

        messages = [SystemMessage(content=system_text)] + list(state["messages"])

        structured_llm = self.llm.with_structured_output(StructuredPlanOutput)
        result: StructuredPlanOutput = await structured_llm.ainvoke(messages)

        ai_msg = AIMessage(content=result.ai_feedback or "已为你生成计划。")

        return {
            "messages": [ai_msg],
            "structured_output": result,
            "natural_output": result.ai_feedback or "",
        }

    # ── public interface ──────────────────────────────────────────

    async def ainvoke(self, state: PlanGeneratorState) -> dict:
        return await self.graph.ainvoke(state)

    async def astream(self, state: PlanGeneratorState):
        async for chunk in self.graph.astream(state):
            yield chunk
