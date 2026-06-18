"""Shared tree-sitter factory for all non-Python language extractors."""
import importlib

from tree_sitter import Language, Parser, Query, QueryCursor


def make_ts_extractor(ts_lang_name: str, query_str: str):
    """Return an extractor function for the given tree-sitter language.

    Args:
        ts_lang_name: Name of the tree_sitter_<name> package (e.g. "go", "rust").
        query_str: Tree-sitter query that captures @fn (the full function node)
                   and @name (the identifier node for the function name).

    Returns:
        extractor(lines, lang_cfg) -> list of (name, start_0based, end_0based)
    """
    mod = importlib.import_module(f"tree_sitter_{ts_lang_name}")
    lang = Language(mod.language())
    parser = Parser(lang)
    query = Query(lang, query_str)

    def extractor(lines, lang_cfg):
        source = "\n".join(lines).encode("utf-8")
        tree = parser.parse(source)
        cursor = QueryCursor(query)

        results = []
        # matches() yields (pattern_index, {capture_name: [Node, ...]}) per match
        for _pattern_idx, captures in cursor.matches(tree.root_node):
            fn_list = captures.get("fn", [])
            name_list = captures.get("name", [])
            if not fn_list or not name_list:
                continue
            fn_node = fn_list[0]
            name = name_list[0].text.decode("utf-8")
            start = fn_node.start_point[0]  # (row, col) — row is 0-based
            end = fn_node.end_point[0]
            results.append((name, start, end))

        return results

    return extractor
