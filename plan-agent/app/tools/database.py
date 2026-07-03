from langchain.tools import tool


@tool
def query_database(sql: str) -> str:
    """Execute a read-only SQL query against the plan database. Reserved for future use."""
    # TODO: implement database query with read-only safety
    return "[]"
