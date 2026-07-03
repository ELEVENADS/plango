from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single message in the conversation."""
    role: str = Field(..., pattern="^(user|assistant)$", description="消息角色")
    content: str = Field(..., description="消息内容")


class PlanGenerateRequest(BaseModel):
    """Request for plan generation via conversation."""
    user_id: int = Field(..., description="用户 ID")
    messages: list[ChatMessage] = Field(..., min_length=1, description="对话消息列表，最后一条为当前用户输入")
