from datetime import date, time
from typing import Any

from pydantic import BaseModel, Field


class PlanSyncRequest(BaseModel):
    plan_id: int = Field(..., description="计划 ID")
    user_id: int = Field(..., description="用户 ID")
    title: str = Field(..., max_length=200, description="计划标题")
    description: str = Field(default="", description="详细描述")
    plan_date: str | None = Field(default=None, description="计划执行日期 YYYY-MM-DD")
    start_time: str | None = Field(default=None, description="开始时间 HH:MM")
    end_time: str | None = Field(default=None, description="结束时间 HH:MM")
    priority: int = Field(default=0, description="优先级: 0=低, 1=中, 2=高")
    status: str = Field(default="", description="计划状态")
    tags: str = Field(default="", description="标签，逗号分隔")
    ai_feedback: str = Field(default="", description="AI 反馈")
    ai_generated: bool = Field(default=False, description="是否 AI 生成")
    deleted: bool = Field(default=False, description="是否已删除")
    ext_info: dict[str, Any] | None = Field(default=None, description="扩展信息")
    created_at: str | None = Field(default=None, description="创建时间")
    updated_at: str | None = Field(default=None, description="更新时间")

    def to_plan_dict(self) -> dict:
        return self.model_dump(exclude_none=True)
