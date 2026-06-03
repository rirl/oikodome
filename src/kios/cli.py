#!/usr/bin/env python3
"""kios CLI module.

Provides commands: investigate, status, investigate-prompt
"""
from pathlib import Path
from datetime import datetime
import typer

app = typer.Typer(help="Knowledge Investigation Operating System (KIOS)")

INVESTIGATIONS_DIR = Path("investigations")


def slugify(text: str) -> str:
    """Return a URL-friendly slug for the given text."""
    return text.lower().strip().replace(" ", "-").replace("/", "-")


@app.command()
def investigate(topic: str):
    """Create a new investigation directory and write a basic investigation file.

    The command creates the investigation directory structure and writes an
    `investigation.adoc` file containing metadata and the question.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    investigation_id = f"INV-{timestamp}"
    investigation_path = INVESTIGATIONS_DIR / f"{investigation_id}-{slugify(topic)}"

    (investigation_path / "prompts").mkdir(parents=True, exist_ok=True)
    (investigation_path / "responses").mkdir(exist_ok=True)
    (investigation_path / "evidence").mkdir(exist_ok=True)
    (investigation_path / "claims").mkdir(exist_ok=True)
    (investigation_path / "notes").mkdir(exist_ok=True)

    investigation_file = investigation_path / "investigation.adoc"

    investigation_file.write_text(
        f"""= Investigation

ID:: {investigation_id}

Title:: {topic}

Status:: Active

Created:: {datetime.now().isoformat()}

== Question

{topic}
"""
    )

    typer.echo(f"Created: {investigation_id}")
    typer.echo(f"Location: {investigation_path}")


@app.command()
def status():
    """Print a summary of investigations in the investigations directory."""
    INVESTIGATIONS_DIR.mkdir(exist_ok=True)

    investigations = [p for p in INVESTIGATIONS_DIR.iterdir() if p.is_dir()]

    typer.echo(f"Investigations: {len(investigations)}")

    for inv in investigations:
        typer.echo(f"  - {inv.name}")


@app.command("investigate-prompt")
def investigate_prompt(topic: str, template: str = "default"):
    """Create a prompt file for a new investigation.

    This command creates the investigation directory structure (if not present)
    and writes a prompt file into the `prompts/` folder under the new investigation.

    Arguments:
        topic: The investigation topic or question.
        template: The prompt template variant to use (default: "default").
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    investigation_id = f"INV-{timestamp}"
    slug = slugify(topic)
    investigation_path = INVESTIGATIONS_DIR / f"{investigation_id}-{slug}"

    # create folders
    (investigation_path / "prompts").mkdir(parents=True, exist_ok=True)
    (investigation_path / "responses").mkdir(exist_ok=True)
    (investigation_path / "evidence").mkdir(exist_ok=True)
    (investigation_path / "claims").mkdir(exist_ok=True)
    (investigation_path / "notes").mkdir(exist_ok=True)

    # build prompt content
    prompt_content = (
        f"# Investigation Prompt\n\nTopic: {topic}\n\n"
        "Please produce a structured investigation plan that includes:\n"
        "- A concise hypothesis or set of questions to investigate\n"
        "- Data sources to consult and why\n"
        "- Suggested experiments or checks to run\n"
        "- Expected outcomes and how to validate them\n"
    )

    prompt_file = investigation_path / "prompts" / f"prompt-{timestamp}.md"
    prompt_file.write_text(prompt_content)

    typer.echo(f"Created: {investigation_id}")
    typer.echo(f"Location: {investigation_path}")
    typer.echo(f"Prompt: {prompt_file}")


def main():
    """Console entrypoint for the kios package (used by console_scripts)."""
    app()


if __name__ == "__main__":
    main()
    