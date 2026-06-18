"""Tests for the Go function extractor (tree-sitter-based)."""
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "go"


def _extract(source: str):
    from src.extractors.go import extract_go
    lines = source.splitlines()
    return [(name, start, end) for name, start, end in extract_go(lines, {})]


def _names(source: str):
    return [name for name, _, _ in _extract(source)]


# ---------------------------------------------------------------------------
# Basic cases
# ---------------------------------------------------------------------------

def test_basic_function():
    src = "package p\nfunc Foo(x int) int {\n\treturn x\n}\n"
    assert "Foo" in _names(src)


def test_unexported_function():
    src = "package p\nfunc bar() {}\n"
    assert "bar" in _names(src)


def test_multiple_functions():
    src = "package p\nfunc A() {}\nfunc B() {}\nfunc C() {}\n"
    assert _names(src) == ["A", "B", "C"]


def test_multi_return():
    src = "package p\nfunc Split(x int) (int, error) {\nreturn x, nil\n}\n"
    assert "Split" in _names(src)


# ---------------------------------------------------------------------------
# Methods (receiver functions)
# ---------------------------------------------------------------------------

def test_value_receiver_method():
    src = "package p\ntype T struct{}\nfunc (t T) Hello() string {\nreturn \"\"\n}\n"
    assert "Hello" in _names(src)


def test_pointer_receiver_method():
    src = "package p\ntype T struct{}\nfunc (t *T) Reset() {\n}\n"
    assert "Reset" in _names(src)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_func_in_comment_not_extracted():
    src = "package p\n// func fakeInComment() {}\nfunc Real() {}\n"
    names = _names(src)
    assert "fakeInComment" not in names
    assert "Real" in names


def test_func_in_backtick_string_not_extracted():
    """func inside a Go backtick string must NOT be treated as a function."""
    src = "package p\nvar s = `\nfunc fake() {}\n`\nfunc Real() {}\n"
    names = _names(src)
    assert "fake" not in names
    assert "Real" in names


def test_empty_file():
    assert _names("") == []


def test_no_functions():
    src = "package p\nvar x = 1\n"
    assert _names(src) == []


# ---------------------------------------------------------------------------
# Fixture file (integration)
# ---------------------------------------------------------------------------

def test_fixture_file():
    src = (FIXTURE_DIR / "basic.go").read_text()
    names = _names(src)
    expected = {"Add", "subtract", "MultiReturn", "Increment", "Reset", "noParams"}
    assert expected.issubset(set(names)), f"Missing: {expected - set(names)}"
    assert "fakeInComment" not in names
