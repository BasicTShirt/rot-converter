# tests/test_b_rot.py
import pytest
from rot_converter.converter import ROTConvertor


@pytest.fixture
def converter():
    return ROTConvertor()


class TestBRot:
    # --- Basic tests (built-in languages) ---

    def test_returns_dict(self, converter):
        result = converter.b_rot("abc", "en")
        assert isinstance(result, dict)
        assert len(result) == 26

    def test_contains_all_keys(self, converter):
        result = converter.b_rot("abc", "en")
        assert set(result.keys()) == set(range(26))

    def test_zero_key_matches_original(self, converter):
        result = converter.b_rot("Hello", "en")
        assert result[0] == "Hello"

    def test_full_bruteforce_cycle(self, converter):
        encrypted = converter.m_rot("Secret", 7, "en")
        result = converter.b_rot(encrypted, "en")
        assert "Secret" in result.values()

    def test_preserve_non_alphabet(self, converter):
        result = converter.b_rot("Hi!", "en")
        assert all("!" in v for v in result.values())

    def test_russian_bruteforce(self, converter):
        result = converter.b_rot("АБ", "ru")
        ru_len = len(converter.alphabets["ru"])
        assert len(result) == ru_len
        assert result[0] == "АБ"

    # --- Custom alphabet tests ---

    def test_custom_alphabet_returns_dict(self, converter):
        result = converter.b_rot("abc", "ABCDEF")
        assert isinstance(result, dict)
        assert len(result) == 6

    def test_custom_alphabet_all_keys(self, converter):
        result = converter.b_rot("abc", "ABCDEF")
        assert set(result.keys()) == set(range(6))

    def test_custom_alphabet_zero_key(self, converter):
        result = converter.b_rot("Hello!", "HELO")
        assert result[0] == "Hello!"

    def test_custom_alphabet_bruteforce_cycle(self, converter):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        encrypted = converter.m_rot("HELLO", 5, alphabet)
        result = converter.b_rot(encrypted, alphabet)
        assert "HELLO" in result.values()

    def test_custom_alphabet_preserve_non_alphabet(self, converter):
        result = converter.b_rot("a-b_c", "ABC")
        assert all("-" in v and "_" in v for v in result.values())

    def test_custom_alphabet_short(self, converter):
        result = converter.b_rot("AB", "AB")
        assert len(result) == 2
        assert result[0] == "AB"
        assert result[1] == "BA"


class TestBRotErrors:
    def test_empty_string(self, converter):
        with pytest.raises(ValueError, match="did not enter a string"):
            converter.b_rot("", "en")

    def test_none_string(self, converter):
        with pytest.raises(ValueError, match="did not enter a string"):
            converter.b_rot(None, "en")

    def test_empty_language_and_alphabet(self, converter):
        with pytest.raises(ValueError, match="did not enter a language or a custom alphabet"):
            converter.b_rot("test", "")

    def test_none_language_and_alphabet(self, converter):
        with pytest.raises(ValueError, match="did not enter a language or a custom alphabet"):
            converter.b_rot("test", None)

    def test_language_not_string(self, converter):
        with pytest.raises(ValueError, match="not a string"):
            converter.b_rot("test", 123)