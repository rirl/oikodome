#!/usr/bin/env python3
""
Generate a codegen prompt from a Markdown file.
""
from pathlib import Path
import sys
if len(sys.argv) < 2:
    print("Usage: generate_prompt_from_md.py README.md --task \"Task\"")
    sys.exit(2)
md = Path(sys.argv[1]).read_text(encoding='utf8')
if '--task' in sys.argv:
    task = sys.argv[sys.argv.index('--task') + 1]
else:
    task = 'Generate code according to the project context'
safe_md = md.replace('"', '\\"\\"\\"')
prompt = f"You are an expert software engineer and code generator. Use the following project context and instructions to produce the requested output.

Project context (Markdown):
---
{safe_md}
---

Task:
{task}

Requirements and rules:
- When generating Python code, use triple double-quote docstrings exclusively for module, class, function, and method docstrings (use triple double-quotes: \"\"\"). Do not use triple single-quotes (''') or malformed quotes.
- Preserve existing indentation and keep code style consistent.
- Provide only the requested files/changes. Do not include extra commentary outside the requested file content.
- If you generate files, provide their file path(s) and full content, using valid Python syntax.
- If the docstring would include triple double-quotes, escape them as \"\"\" inside the content.
- If asked to create tests, use pytest and include a small focused test.
- Keep the output concise and machine-parseable. If you supply multiple files, indicate each file path before its contents.

Output format:
- If generating code files, return them as separate content blocks labeled with the target file path.
- If generating a single prompt or snippet, return only the prompt text with no extra commentary.

Produce the requested result now.
""
print(prompt)
