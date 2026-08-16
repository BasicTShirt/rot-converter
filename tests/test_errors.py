# tests/test_errors.py
import pytest
from rot_converter.converter import ROTConvertor

@pytest.fixture
def converter():
    return ROTConvertor()

class TestErrors:
    def test_none_string(self, converter):
        with pytest.raises(ValueError, match="did not enter a string"):
            converter.m_rot(None, 1, "en")

    def test_none_language(self, converter):
        with pytest.raises(ValueError, match="did not enter a language"):
            converter.m_rot("test", 1, None)

    def test_language_not_string(self, converter):
        with pytest.raises(ValueError, match="not a string"):
            converter.m_rot("test", 1, 123)

    def test_none_key(self, converter):
        with pytest.raises(ValueError, match="did not enter a key"):
            converter.m_rot("test", None, "en")

    def test_key_not_int(self, converter):
        with pytest.raises(ValueError, match="not a integer"):
            converter.m_rot("test", "1", "en")

    def test_empty_language(self, converter):
        with pytest.raises(ValueError, match="did not enter a language"):
            converter.m_rot("test", 1, "")

    def test_multiple_errors(self, converter):
        with pytest.raises(ValueError) as exc:
            converter.m_rot("", None, "")
        err = str(exc.value)
        assert "did not enter a string" in err
        assert "did not enter a language" in err
        assert "did not enter a key" in err