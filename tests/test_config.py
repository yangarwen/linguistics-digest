import os
import pytest

from slang_digest.config import load_config


BASE_ENV = {
    "SMTP_HOST": "smtp.example.com",
    "SMTP_PORT": "587",
    "SMTP_USERNAME": "user",
    "SMTP_PASSWORD": "pass",
    "EMAIL_FROM": "from@example.com",
    "EMAIL_TO": "to@example.com",
}


class TestLoadConfig:
    def test_loads_required_fields(self, monkeypatch):
        for k, v in BASE_ENV.items():
            monkeypatch.setenv(k, v)
        config = load_config()
        assert config.smtp_host == "smtp.example.com"
        assert config.smtp_port == 587
        assert config.email_from == "from@example.com"
        assert config.email_to == "to@example.com"

    def test_raises_on_missing_required_var(self, monkeypatch):
        for k, v in BASE_ENV.items():
            monkeypatch.setenv(k, v)
        monkeypatch.delenv("SMTP_HOST")
        with pytest.raises(ValueError, match="SMTP_HOST"):
            load_config()

    def test_default_subject(self, monkeypatch):
        for k, v in BASE_ENV.items():
            monkeypatch.setenv(k, v)
        monkeypatch.delenv("EMAIL_SUBJECT", raising=False)
        config = load_config()
        assert "Slang" in config.email_subject

    def test_custom_subject(self, monkeypatch):
        for k, v in BASE_ENV.items():
            monkeypatch.setenv(k, v)
        monkeypatch.setenv("EMAIL_SUBJECT", "My Custom Subject")
        config = load_config()
        assert config.email_subject == "My Custom Subject"

    def test_bad_words_empty_by_default(self, monkeypatch):
        for k, v in BASE_ENV.items():
            monkeypatch.setenv(k, v)
        monkeypatch.delenv("BAD_WORDS", raising=False)
        config = load_config()
        assert config.bad_words == []

    def test_bad_words_parsed_from_env(self, monkeypatch):
        for k, v in BASE_ENV.items():
            monkeypatch.setenv(k, v)
        monkeypatch.setenv("BAD_WORDS", "foo, bar, baz")
        config = load_config()
        assert config.bad_words == ["foo", "bar", "baz"]

    def test_bad_words_strips_whitespace(self, monkeypatch):
        for k, v in BASE_ENV.items():
            monkeypatch.setenv(k, v)
        monkeypatch.setenv("BAD_WORDS", "  foo  ,  bar  ")
        config = load_config()
        assert config.bad_words == ["foo", "bar"]
