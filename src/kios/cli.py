from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import sys


def slugify(value: str) -> str:
    normalized = value.lower().strip()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    return normalized or "investigation"


def create_investigation(prompt: str, root: Path | None = None) -> Path:
    investigations_root = root or Path("investigations")
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(prompt)
    path = investigations_root / f"{date_prefix}-{slug}"
    path.mkdir(parents=True, exist_ok=True)

    metadata = f"""id: {date_prefix}-{slug}
title: {prompt}
status: draft
created: {datetime.now().isoformat(timespec="seconds")}
provenance:
  persistence: git
  format: asciidoc
"""

    (path / "metadata.yaml").write_text(metadata, encoding="utf-8")
    (path / "prompt.adoc").write_text(
        f"= Investigation Prompt\n\n{prompt}\n", encoding="utf-8"
    )
    (path / "research-log.adoc").write_text("= Research Log\n\nTODO\n", encoding="utf-8")
    (path / "report.adoc").write_text("= Investigation Report\n\nTODO\n", encoding="utf-8")
    return path


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: kios investigate <prompt>")
        raise SystemExit(1)

    command = sys.argv[1]
    if command != "investigate":
        print(f"Unknown command: {command}")
        raise SystemExit(1)

    prompt = " ".join(sys.argv[2:])
    path = create_investigation(prompt)
    print(f"Created investigation: {path}")


if __name__ == "__main__":
    main()
