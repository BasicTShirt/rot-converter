# tests/test_m_rot.py
import pytest
from rot_converter.converter import ROTConvertor


@pytest.fixture
def converter():
    return ROTConvertor()


class TestMRot:
    # --- Basic tests (built-in languages) ---

    def test_basic_english(self, converter):
        assert converter.m_rot("Hello", 13, "en") == "Uryyb"
        assert converter.m_rot("abc", 1, "en") == "bcd"
        assert converter.m_rot("XYZ", 3, "en") == "ABC"

    def test_preserve_case(self, converter):
        assert converter.m_rot("AbC", 1, "en") == "BcD"

    def test_preserve_non_alphabet(self, converter):
        assert converter.m_rot("Hello, World! 123", 13, "en") == "Uryyb, Jbeyq! 123"

    def test_russian(self, converter):
        assert converter.m_rot("АБВ", 1, "ru") == "БВГ"
        assert converter.m_rot("Привет", 3, "ru") == "Тулезх"

    def test_full_rotation(self, converter):
        alphabet_len = len(converter.alphabets["en"])
        assert converter.m_rot("Test", alphabet_len, "en") == "Test"

    def test_negative_key(self, converter):
        assert converter.m_rot("bcd", -1, "en") == "abc"

    def test_zero_key(self, converter):
        assert converter.m_rot("Hello", 0, "en") == "Hello"

    # --- Custom alphabet tests ---

    def test_custom_alphabet_basic(self, converter):
        assert converter.m_rot("ABC", 1, "ABCDEF") == "BCD"
        assert converter.m_rot("ABC", -1, "ABCDEF") == "FAB"

    def test_custom_alphabet_case_preserve(self, converter):
        assert converter.m_rot("AbC", 1, "ABC") == "BcA"

    def test_custom_alphabet_non_alphabet_preserve(self, converter):
        assert converter.m_rot("A-B!C", 1, "ABC") == "B-C!A"

    def test_custom_alphabet_full_rotation(self, converter):
        alphabet = "0123456789"
        assert converter.m_rot("123", 10, alphabet) == "123"

    def test_custom_alphabet_base36(self, converter):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        assert converter.m_rot("ABC", 1, alphabet) == "BCD"
        assert converter.m_rot("XYZ", 1, alphabet) == "YZ0"
        assert converter.m_rot("789", 1, alphabet) == "89A"

    def test_custom_alphabet_with_unicode(self, converter):
        alphabet = "АБВГДЕЁЖЗ"
        assert converter.m_rot("АБВ", 2, alphabet) == "ВГД"

    def test_custom_alphabet_hebrew(self, converter):
        alphabet = "אבגדהוזחט"
        assert converter.m_rot("אבג", 1, alphabet) == "בגד"


class TestMRotErrors:
    def test_empty_string(self, converter):
        with pytest.raises(ValueError, match="did not enter a string"):
            converter.m_rot("", 1, "en")

    def test_none_string(self, converter):
        with pytest.raises(ValueError, match="did not enter a string"):
            converter.m_rot(None, 1, "en")

    def test_empty_language_and_alphabet(self, converter):
        with pytest.raises(ValueError, match="did not enter a language or a custom alphabet"):
            converter.m_rot("test", 1, "")

    def test_none_language_and_alphabet(self, converter):
        with pytest.raises(ValueError, match="did not enter a language or a custom alphabet"):
            converter.m_rot("test", 1, None)

    def test_language_not_string(self, converter):
        with pytest.raises(ValueError, match="not a string"):
            converter.m_rot("test", 1, 123)

    def test_none_key(self, converter):
        with pytest.raises(ValueError, match="did not enter a key"):
            converter.m_rot("test", None, "en")

    def test_key_not_int(self, converter):
        with pytest.raises(ValueError, match="not a integer"):
            converter.m_rot("test", 1.5, "en")