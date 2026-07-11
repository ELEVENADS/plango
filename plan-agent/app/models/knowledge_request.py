from typing import Any

from pydantic import BaseModel, Field


class KnowledgeSyncRequest(BaseModel):
    doc_id: str = Field(..., description="文档唯一 ID")
    user_id: int = Field(..., description="用户 ID")
    doc_type: str = Field(..., description="文档类型: preference / rule / resource")
    title: str = Field(..., max_length=200, description="文档标题")
    content: str = Field(..., description="文档正文")
    tags: str = Field(default="", description="标签，逗号分隔")
    source: str = Field(default="manual", description="来源: manual / upload / system")
    metadata: dict[str, Any] | str | None = Field(default=None, description="扩展元数据")
    deleted: bool = Field(default=False, description="是否已删除")
    created_at: str | None = Field(default=None, description="创建时间")
    updated_at: str | None = Field(default=None, description="更新时间")

    def to_doc_dict(self) -> dict:
        return self.model_dump(exclude_none=True)
