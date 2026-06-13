from slang_digest.mailer import _sanitize, build_email_body, build_html_body

SAMPLE_SLANG = [
    {"word": "glow-up", "definition": "A positive transformation."},
    {"word": "no cap", "definition": "No lie, I'm serious."},
]
SAMPLE_QUOTE = {"text": "Be the change you wish to see.", "author": "Gandhi"}


class TestSanitize:
    def test_empty_bad_words_returns_text_unchanged(self):
        assert _sanitize("hello world", []) == "hello world"

    def test_replaces_matching_word_with_asterisks(self):
        result = _sanitize("This is bad stuff", ["bad"])
        assert result == "This is *** stuff"

    def test_preserves_length_of_replaced_word(self):
        result = _sanitize("hello", ["hello"])
        assert result == "*****"

    def test_case_insensitive_replacement(self):
        result = _sanitize("BAD bad Bad", ["bad"])
        assert result == "*** *** ***"

    def test_does_not_replace_substrings(self):
        result = _sanitize("badger", ["bad"])
        assert result == "badger"

    def test_multiple_bad_words(self):
        result = _sanitize("foo and bar", ["foo", "bar"])
        assert result == "*** and ***"

    def test_empty_string(self):
        assert _sanitize("", ["bad"]) == ""


class TestBuildEmailBody:
    def test_contains_quote_text_and_author(self):
        body = build_email_body(SAMPLE_SLANG, SAMPLE_QUOTE, [])
        assert SAMPLE_QUOTE["text"] in body
        assert SAMPLE_QUOTE["author"] in body

    def test_contains_slang_words(self):
        body = build_email_body(SAMPLE_SLANG, SAMPLE_QUOTE, [])
        assert "glow-up" in body
        assert "no cap" in body

    def test_sanitizes_slang_words(self):
        body = build_email_body(SAMPLE_SLANG, SAMPLE_QUOTE, ["glow-up"])
        assert "glow-up" not in body
        assert "******" in body

    def test_sanitizes_quote_text(self):
        body = build_email_body(SAMPLE_SLANG, SAMPLE_QUOTE, ["change"])
        assert "change" not in body

    def test_sanitizes_quote_author(self):
        body = build_email_body(SAMPLE_SLANG, SAMPLE_QUOTE, ["Gandhi"])
        assert "Gandhi" not in body

    def test_numbered_list(self):
        body = build_email_body(SAMPLE_SLANG, SAMPLE_QUOTE, [])
        assert "1." in body
        assert "2." in body


class TestBuildHtmlBody:
    def test_contains_quote_text_and_author(self):
        html = build_html_body(SAMPLE_SLANG, SAMPLE_QUOTE, [])
        assert SAMPLE_QUOTE["text"] in html
        assert SAMPLE_QUOTE["author"] in html

    def test_contains_slang_words(self):
        html = build_html_body(SAMPLE_SLANG, SAMPLE_QUOTE, [])
        assert "glow-up" in html
        assert "no cap" in html

    def test_sanitizes_slang_in_html(self):
        html = build_html_body(SAMPLE_SLANG, SAMPLE_QUOTE, ["glow-up"])
        assert "glow-up" not in html

    def test_sanitizes_quote_text_in_html(self):
        html = build_html_body(SAMPLE_SLANG, SAMPLE_QUOTE, ["change"])
        assert "change" not in html

    def test_sanitizes_quote_author_in_html(self):
        html = build_html_body(SAMPLE_SLANG, SAMPLE_QUOTE, ["Gandhi"])
        assert "Gandhi" not in html

    def test_is_valid_html_structure(self):
        html = build_html_body(SAMPLE_SLANG, SAMPLE_QUOTE, [])
        assert "<html>" in html
        assert "<ol>" in html
        assert "<blockquote" in html
