#!/usr/bin/env python3
"""Run a prompt from a Markdown file through the OpenAI Chat API.

Usage:
  python scripts/run_prompt_from_md.py README.md --model gpt-4 --dry
Reads the markdown file, prepends a persistent system rule (from scripts/prompt_rules.txt
if present), and sends messages to the model. Use --dry to print assembled messages.
"""
import argparse
import os
import sys
try:
    import openai
except Exception:
    openai = None
RULE_PATH = 'scripts/prompt_rules.txt'
DEFAULT_RULE = (
    'When generating Python files, always use triple double-quote docstrings (""") for module, class, '
    'function, and method docstrings. Do not use triple single-quotes (\'\'\'). Return only the file contents.'
)

def read_md(path):
    return open(path, 'r', encoding='utf8').read()

def build_messages(system_rule, md):
    return [
        {"role": "system", "content": system_rule},
        {"role": "user", "content": f"Project context (Markdown):\n---\n{md}\n---"},
    ]

def call_model(messages, model='gpt-4'):
    if openai is None:
        raise RuntimeError('openai package not installed')
    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        raise RuntimeError('OPENAI_API_KEY not set')
    openai.api_key = key
    resp = openai.ChatCompletion.create(model=model, messages=messages)
    return resp['choices'][0]['message']['content']

def main():
    p = argparse.ArgumentParser()
    p.add_argument('md', help='Markdown file to send as prompt/context')
    p.add_argument('--model', default='gpt-4')
    p.add_argument('--dry', action='store_true')
    args = p.parse_args()

    if not os.path.exists(args.md):
        print('Markdown file not found:', args.md, file=sys.stderr)
        return 2
    md = read_md(args.md)
    system_rule = open(RULE_PATH, 'r', encoding='utf8').read().strip() if os.path.exists(RULE_PATH) else DEFAULT_RULE
    messages = build_messages(system_rule, md)

    if args.dry:
        import json
        print(json.dumps(messages, indent=2, ensure_ascii=False))
        return 0
    out = call_model(messages, model=args.model)
    print(out)
    return 0
if __name__ == '__main__':
    sys.exit(main())