from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):

    @abstractmethod
    async def ainvoke(self, state: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    async def astream(self, state: dict[str, Any]):
        ...
