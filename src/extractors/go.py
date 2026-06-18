"""Go function extractor using tree-sitter."""
from src.extractors._treesitter import make_ts_extractor

_GO_QUERY = """
(function_declaration name: (identifier) @name) @fn
(method_declaration name: (field_identifier) @name) @fn
"""

extract_go = make_ts_extractor("go", _GO_QUERY)
