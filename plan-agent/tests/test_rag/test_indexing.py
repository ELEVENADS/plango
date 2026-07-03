import pytest

from app.rag.indexing import build_mapping, create_index, delete_index, refresh_index


class TestBuildMapping:
    def test_default_dims(self) -> None:
        mapping = build_mapping()
        assert "mappings" in mapping
        assert "settings" in mapping
        props = mapping["mappings"]["properties"]
        assert props["plan_id"]["type"] == "long"
        assert props["user_id"]["type"] == "long"
        assert props["title"]["type"] == "text"
        assert "keyword" in props["title"]["fields"]
        assert props["priority"]["type"] == "integer"
        assert props["deleted"]["type"] == "boolean"
        assert props["embedding"]["type"] == "dense_vector"
        assert props["embedding"]["similarity"] == "cosine"
        assert props["embedding"]["dims"] == 1536

    def test_custom_dims(self) -> None:
        mapping = build_mapping(dims=1024)
        assert mapping["mappings"]["properties"]["embedding"]["dims"] == 1024

    def test_date_format(self) -> None:
        mapping = build_mapping()
        date_prop = mapping["mappings"]["properties"]["plan_date"]
        assert date_prop["format"] == "yyyy-MM-dd"

    def test_text_fields_have_ik_analyzer(self) -> None:
        mapping = build_mapping()
        for field in ("title", "description", "tags"):
            props = mapping["mappings"]["properties"][field]
            assert props["analyzer"] == "ik_max_word"
            assert props["search_analyzer"] == "ik_smart"


class TestCreateIndex:
    def test_creates_when_not_exists(self, mock_es) -> None:
        mock_es.indices.exists.return_value = False
        result = create_index(mock_es, "test_index")
        assert result == "test_index"
        mock_es.indices.create.assert_called_once()

    def test_skips_when_exists(self, mock_es) -> None:
        mock_es.indices.exists.return_value = True
        result = create_index(mock_es, "test_index")
        assert result == "test_index"
        mock_es.indices.create.assert_not_called()


class TestDeleteIndex:
    def test_deletes_when_exists(self, mock_es) -> None:
        mock_es.indices.exists.return_value = True
        delete_index(mock_es, "test_index")
        mock_es.indices.delete.assert_called_once_with(index="test_index")

    def test_skips_when_not_exists(self, mock_es) -> None:
        mock_es.indices.exists.return_value = False
        delete_index(mock_es, "test_index")
        mock_es.indices.delete.assert_not_called()


class TestRefreshIndex:
    def test_refresh(self, mock_es) -> None:
        refresh_index(mock_es, "test_index")
        mock_es.indices.refresh.assert_called_once_with(index="test_index")
