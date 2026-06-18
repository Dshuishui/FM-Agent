"""Tests for the Python function extractor (ast-based)."""
import pytest
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "python"


def _extract(source: str):
    """Helper: run the Python extractor on a source string, return list of (name, start, end)."""
    from src.extractors.python import extract_python
    lines = source.splitlines()
    return [(name, start, end) for name, start, end in extract_python(lines, {})]


def _names(source: str):
    return [name for name, _, _ in _extract(source)]


# ---------------------------------------------------------------------------
# Basic cases
# ---------------------------------------------------------------------------

def test_basic_functions():
    src = "def foo(x):\n    return x\n\ndef bar():\n    pass\n"
    assert _names(src) == ["foo", "bar"]


def test_async_def():
    """async def must be extracted — old regex-based impl missed this."""
    src = "async def fetch(url):\n    pass\n"
    assert _names(src) == ["fetch"]


def test_mixed_sync_async():
    src = "def sync():\n    pass\n\nasync def async_fn():\n    pass\n"
    assert _names(src) == ["sync", "async_fn"]


# ---------------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------------

def test_single_decorator_included_in_range():
    src = "@staticmethod\ndef greet():\n    pass\n"
    results = _extract(src)
    assert len(results) == 1
    name, start, end = results[0]
    assert name == "greet"
    assert start == 0          # decorator line is line 0


def test_multiple_decorators():
    src = "@decorator_a\n@decorator_b\ndef multi():\n    pass\n"
    results = _extract(src)
    assert results[0][0] == "multi"
    assert results[0][1] == 0  # starts at first decorator


# ---------------------------------------------------------------------------
# Multi-line signatures
# ---------------------------------------------------------------------------

def test_multiline_signature():
    src = (
        "def long_fn(\n"
        "    a: int,\n"
        "    b: str,\n"
        ") -> bool:\n"
        "    return True\n"
    )
    assert _names(src) == ["long_fn"]


# ---------------------------------------------------------------------------
# Nested functions
# ---------------------------------------------------------------------------

def test_nested_functions_both_extracted():
    src = "def outer():\n    def inner():\n        pass\n    return inner\n"
    names = _names(src)
    assert "outer" in names
    assert "inner" in names


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_def_inside_string_not_extracted():
    """def inside a string literal must NOT be treated as a function."""
    src = 'sql = """\ndef fake():\n    pass\n"""\n'
    assert _names(src) == []


def test_syntax_error_returns_empty():
    """A file with a syntax error must not raise — return empty list."""
    src = "def broken(\n    return 1\n"
    assert _names(src) == []


def test_empty_file():
    assert _names("") == []


def test_no_functions():
    src = "x = 1\nprint(x)\n"
    assert _names(src) == []


# ---------------------------------------------------------------------------
# Fixture file (integration)
# ---------------------------------------------------------------------------

def test_fixture_file():
    """Run extractor on the full fixture file and verify expected functions."""
    src = (FIXTURE_DIR / "basic.py").read_text()
    names = _names(src)
    expected = {
        "add", "subtract", "fetch",
        "greet", "multi_decorated",
        "outer", "inner",
        "long_signature",
    }
    assert expected.issubset(set(names)), f"Missing: {expected - set(names)}"
    assert "fake_in_string" not in names
