#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import typer

app = typer.Typer(help="Knowledge Investigation Operating System (KIOS)")

INVESTIGATIONS_DIR = Path("investigations")

def slugify(text: str) -> str:
    return text.lower().strip().replace(" ", "-").replace("/", "-")

@app.command()
def investigate(topic: str):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    investigation_id = f"INV-{timestamp}"
    investigation_path = INVESTIGATIONS_DIR / f"{investigation_id}-{slugify(topic)}"

    (investigation_path / "prompts").mkdir(parents=True, exist_ok=True)
    (investigation_path / "responses").mkdir(exist_ok=True)
    (investigation_path / "evidence").mkdir(exist_ok=True)
    (investigation_path / "claims").mkdir(exist_ok=True)
    (investigation_path / "notes").mkdir(exist_ok=True)

    investigation_file = investigation_path / "investigation.adoc"

    investigation_file.write_text(f'''= Investigation

ID:: {investigation_id}

Title:: {topic}

Status:: Active

Created:: {datetime.now().isoformat()}

== Question

{topic}
''')

    typer.echo(f"Created: {investigation_id}")
    typer.echo(f"Location: {investigation_path}")

@app.command()
def status():
    INVESTIGATIONS_DIR.mkdir(exist_ok=True)

    investigations = [p for p in INVESTIGATIONS_DIR.iterdir() if p.is_dir()]

    typer.echo(f"Investigations: {len(investigations)}")

    for inv in investigations:
        typer.echo(f"  - {inv.name}")

if __name__ == "__main__":
    app()
