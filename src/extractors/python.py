"""Python function extractor using the built-in ast module."""
import ast


def extract_python(lines, lang_cfg):
    """Extract functions from Python source using ast.

    Returns a list of (function_name, start_line, end_line) tuples,
    where line numbers are 0-based indices into `lines`.
    """
    source = '\n'.join(lines)
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    results = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        # ast uses 1-based line numbers; convert to 0-based
        start = node.lineno - 1
        end = node.end_lineno - 1

        # Include decorators in the function range
        if node.decorator_list:
            start = node.decorator_list[0].lineno - 1

        results.append((node.name, start, end))

    return results
