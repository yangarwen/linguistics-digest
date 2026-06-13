from unittest.mock import MagicMock, patch

from slang_digest.collector import get_daily_quote, get_trending_slang


class TestGetTrendingSlang:
    def _make_ud_response(self, items):
        mock = MagicMock()
        mock.json.return_value = {"list": items}
        return mock

    def test_returns_requested_count(self):
        items = [{"word": f"word{i}", "definition": f"def{i}", "example": ""} for i in range(10)]
        with patch("slang_digest.collector.requests.get", return_value=self._make_ud_response(items)):
            result = get_trending_slang(count=5)
        assert len(result) == 5

    def test_deduplicates_by_word(self):
        items = [{"word": "same", "definition": "def", "example": ""}] * 10
        with patch("slang_digest.collector.requests.get", return_value=self._make_ud_response(items)):
            result = get_trending_slang(count=3)
        # All items have the same word, so only one unique term is found;
        # the rest come from the fallback list
        words = [item["word"] for item in result]
        assert len(words) == len(set(words))

    def test_falls_back_when_api_fails(self):
        with patch("slang_digest.collector.requests.get", side_effect=Exception("network error")):
            result = get_trending_slang(count=3)
        assert len(result) == 3

    def test_falls_back_when_api_returns_empty(self):
        with patch("slang_digest.collector.requests.get", return_value=self._make_ud_response([])):
            result = get_trending_slang(count=3)
        assert len(result) == 3

    def test_result_items_have_word_and_definition(self):
        with patch("slang_digest.collector.requests.get", side_effect=Exception):
            result = get_trending_slang(count=2)
        for item in result:
            assert "word" in item
            assert "definition" in item

    def test_example_appended_to_definition(self):
        items = [{"word": "slay", "definition": "To do something brilliantly.", "example": "She slayed the presentation."}]
        with patch("slang_digest.collector.requests.get", return_value=self._make_ud_response(items)):
            result = get_trending_slang(count=1)
        assert "Example:" in result[0]["definition"]

    def test_no_example_when_empty(self):
        items = [{"word": "slay", "definition": "To do something brilliantly.", "example": ""}]
        with patch("slang_digest.collector.requests.get", return_value=self._make_ud_response(items)):
            result = get_trending_slang(count=1)
        assert "Example:" not in result[0]["definition"]


class TestGetDailyQuote:
    def _make_quote_response(self, content, author):
        mock = MagicMock()
        mock.json.return_value = {"content": content, "author": author}
        return mock

    def test_returns_quote_with_text_and_author(self):
        with patch("slang_digest.collector.requests.get", return_value=self._make_quote_response("Wise words.", "Plato")):
            result = get_daily_quote()
        assert result["text"] == "Wise words."
        assert result["author"] == "Plato"

    def test_falls_back_when_api_fails(self):
        with patch("slang_digest.collector.requests.get", side_effect=Exception("timeout")):
            result = get_daily_quote()
        assert "text" in result
        assert "author" in result
        assert result["text"] != ""
