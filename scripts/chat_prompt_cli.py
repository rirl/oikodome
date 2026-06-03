#!/usr/bin/env python3
"Simple chat wrapper that injects a persistent system rule for Python docstrings.

Usage:
  cat prompt.adoc | python scripts/chat_prompt_cli.py
  python scripts/chat_prompt_cli.py --prompt "Generate kios/cli.py" --dry
""
import argparse
import json
import os
import sys
try:
    import openai
except Exception:
    openai = None
RULE_PATH = 'scripts/prompt_rules.txt'
SYSTEM_RULE = ''
if os.path.exists(RULE_PATH):
    SYSTEM_RULE = open(RULE_PATH, 'r', encoding='utf8').read().strip()
else:
    SYSTEM_RULE = (
        'When generating Python files, always use triple double-quote docstrings (""") for all module, class, function, and method docstrings. '
        'Do NOT use triple single-quotes (\'\'\') or mismatched quotes. If a docstring would include triple double-quotes, escape them as \\\"\\\"\\\" or reformat to preserve valid syntax. Preserve indentation. Return only the file contents.'
    )


def read_stdin_if_needed(provided_prompt: str) -> str:
    if provided_prompt:
        return provided_prompt
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ''


def build_messages(system_rule: str, user_prompt: str, context_md: str = ''):
    messages = [{'role': 'system', 'content': system_rule}]
    if context_md:
        messages.append({'role': 'user', 'content': f'Project context (markdown):\n---\n{context_md}\n---'})
    messages.append({'role': 'user', 'content': user_prompt})
    return messages

def call_openai_chat(messages, model='gpt-4'):
    if openai is None:
        raise RuntimeError('openai package not available')
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY not set')
    openai.api_key = api_key
    resp = openai.ChatCompletion.create(model=model, messages=messages, temperature=0.0)
    return resp['choices'][0]['message']['content']


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--prompt', '-p', help='Prompt text (overrides stdin)')
    p.add_argument('--context', '-c', help='Path to markdown file to include as context')
    p.add_argument('--dry', action='store_true', help='Do not call API; print assembled messages')
    p.add_argument('--model', default='gpt-4')
    args = p.parse_args(argv)

    user_prompt = read_stdin_if_needed(args.prompt)
    if not user_prompt:
        print('No prompt provided via --prompt or stdin', file=sys.stderr)
        return 2
    context_md = ''
    if args.context:
        try:
            context_md = open(args.context, 'r', encoding='utf8').read()
        except Exception as e:
            print('Warning: could not read context file:', e, file=sys.stderr)

    messages = build_messages(SYSTEM_RULE, user_prompt, context_md)

    if args.dry:
        print(json.dumps(messages, indent=2, ensure_ascii=False))
        return 0
    out = call_openai_chat(messages, model=args.model)
    print(out)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
