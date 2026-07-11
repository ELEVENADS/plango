class DocumentChunker:
    """Semantic text chunker using recursive character splitting.

    Short texts (<= chunk_size) are returned as-is (single chunk).
    Long texts are split with overlap to preserve cross-chunk context.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> list[str]:
        """Split text into semantic chunks. Returns at least [text] for short texts."""
        if not text or not text.strip():
            return [text] if text is not None else []

        if len(text) <= self.chunk_size:
            return [text]

        chunks: list[str] = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            if end < len(text):
                end = self._find_split_point(text, start, end)

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(chunk_text)
            start = end - self.chunk_overlap if end < len(text) else end

        return chunks

    def _find_split_point(self, text: str, start: int, end: int) -> int:
        """Walk backward from end to find a natural break point."""
        separators = ["\n\n", "\n", "。", ".", "；", ";", " ", ""]
        search_start = max(start, end - 100)
        for sep in separators:
            if not sep:
                return end
            pos = text.rfind(sep, search_start, end)
            if pos != -1:
                return pos + len(sep)
        return end
