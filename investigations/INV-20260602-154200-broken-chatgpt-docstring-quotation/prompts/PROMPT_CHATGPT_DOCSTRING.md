When generating Python code, use triple double quotes for every docstring (module, class, function, and method), e.g. """This is a docstring.""".
Do not use single quotes or mismatched quotes. If the docstring contains triple double-quotes, escape them or reformat to preserve valid syntax.
Return only the file contents with correct quoting and valid Python syntax.

Example instruction to prepend to your generation prompt:

"When generating Python files, ensure all docstrings use triple double-quotes (\"\"\"). Preserve existing indentation and do not include extraneous commentary. If a docstring would contain triple double-quotes, escape them or use a safe alternative so the resulting file is syntactically valid. Return only the file contents."
