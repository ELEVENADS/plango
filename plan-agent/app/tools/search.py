from langchain.tools import tool

from app.core.config import settings


@tool
def search_historical_plans(query: str, user_id: int) -> str:
    """Search historical plans in Elasticsearch for RAG.

    Args:
        query: Search keywords.
        user_id: The user ID to scope the search.

    Returns:
        JSON string of matching plans.
    """
    # TODO: implement Elasticsearch query
    return "[]"
