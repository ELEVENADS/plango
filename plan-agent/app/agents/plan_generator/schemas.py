from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class PlanItem(BaseModel):
    """A single plan item matching the plan table schema."""
    title: str = Field(..., max_length=200, description="计划标题")
    description: str = Field(default="", description="详细描述")
    plan_date: str = Field(..., description="计划执行日期 YYYY-MM-DD")
    start_time: str = Field(default="", description="计划开始时间 HH:MM")
    end_time: str = Field(default="", description="计划结束时间 HH:MM")
    priority: int = Field(default=0, ge=0, le=2, description="优先级: 0=低, 1=中, 2=高")
    tags: str = Field(default="", description="标签，逗号分隔")


class StructuredPlanOutput(BaseModel):
    """Structured output from the plan generator agent."""
    plans: list[PlanItem] = Field(default_factory=list, description="生成的计划列表")
    ai_feedback: str = Field(default="", description="AI 生成的反馈或建议")


class PlanGeneratorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_id: int
    rag_context: str
    memory_summary: str
    structured_output: StructuredPlanOutput
    natural_output: str
