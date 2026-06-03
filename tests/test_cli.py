from kios import cli

def test_module_exports():
    # Ensure the CLI module exposes the expected Typer app and commands
    assert hasattr(cli, "app")
    assert hasattr(cli, "investigate")
    assert hasattr(cli, "status")
    assert hasattr(cli, "investigate_prompt")
    assert hasattr(cli, "slugify")


def test_investigate_api(monkeypatch, tmp_path, capsys):
    # Test investigate produces the expected filesystem side-effects
    class FixedDateTime:
        @staticmethod
        def now():
            from datetime import datetime as real_datetime
            return real_datetime(2020, 1, 2, 3, 4, 5)

    monkeypatch.setattr(cli, 'INVESTIGATIONS_DIR', tmp_path / "investigations")
    monkeypatch.setattr(cli, 'datetime', FixedDateTime)

    topic = "Full API Test"
    cli.investigate(topic)

    ts = FixedDateTime.now().strftime("%Y%m%d-%H%M%S")
    inv_id = f"INV-{ts}"
    slug = cli.slugify(topic)
    path = tmp_path / "investigations" / f"{inv_id}-{slug}"

    # Directories
    assert (path / "prompts").is_dir()
    assert (path / "responses").is_dir()
    assert (path / "evidence").is_dir()
    assert (path / "claims").is_dir()
    assert (path / "notes").is_dir()

    # investigation file
    inv_file = path / "investigation.adoc"
    assert inv_file.is_file()
    content = inv_file.read_text()
    assert f"ID:: {inv_id}" in content
    assert f"Title:: {topic}" in content
    captured = capsys.readouterr()
    assert f"Created: {inv_id}" in captured.out
    assert f"Location: {path}" in captured.out

def test_investigate_prompt_api(monkeypatch, tmp_path, capsys):
    class FixedDateTime:
        @staticmethod
        def now():
            from datetime import datetime as real_datetime
            return real_datetime(2020, 1, 2, 3, 4, 5)

    monkeypatch.setattr(cli, 'INVESTIGATIONS_DIR', tmp_path / "investigations")
    monkeypatch.setattr(cli, 'datetime', FixedDateTime)

    topic = "Prompt API Test"
    cli.investigate_prompt(topic)

    ts = FixedDateTime.now().strftime("%Y%m%d-%H%M%S")
    inv_id = f"INV-{ts}"
    slug = cli.slugify(topic)
    path = tmp_path / "investigations" / f"{inv_id}-{slug}"

    assert (path / "prompts").is_dir()
    prompts = list((path / "prompts").glob("prompt-*.md"))
    assert len(prompts) == 1
    content = prompts[0].read_text()
    assert f"Topic: {topic}" in content
    assert "- A concise hypothesis" in content
    captured = capsys.readouterr()
    assert f"Created: {inv_id}" in captured.out
    assert "Prompt:" in captured.out

def test_slugify_edge_cases():
    assert cli.slugify("Hello World") == "hello-world"
    assert cli.slugify(" A/B C ") == "a-b-c"
    assert cli.slugify("MixedCASE") == "mixedcase"


def test_investigate_prompt_api(monkeypatch, tmp_path, capsys):
    class FixedDateTime:
        @staticmethod
        def now():
            from datetime import datetime as real_datetime
            return real_datetime(2020, 1, 2, 3, 4, 5)

    monkeypatch.setattr(cli, 'INVESTIGATIONS_DIR', tmp_path / "investigations")
    monkeypatch.setattr(cli, 'datetime', FixedDateTime)

    topic = "Prompt API Test"
    cli.investigate_prompt(topic)

    ts = FixedDateTime.now().strftime("%Y%m%d-%H%M%S")
    inv_id = f"INV-{ts}"
    slug = cli.slugify(topic)
    path = tmp_path / "investigations" / f"{inv_id}-{slug}"

    # Check directories
    assert (path / "prompts").is_dir()
    assert (path / "responses").is_dir()
    assert (path / "evidence").is_dir()
    assert (path / "claims").is_dir()
    assert (path / "notes").is_dir()

    # Check prompt file
    prompt_file = path / "prompts" / f"prompt-{ts}.md"
    assert prompt_file.is_file()
    content = prompt_file.read_text()
    assert f"Topic: {topic}" in content
    assert "Please produce a structured investigation plan" in content
    captured = capsys.readouterr()
    assert f"Created: {inv_id}" in captured.out
    assert f"Location: {path}" in captured.out
    assert f"Prompt: {prompt_file}" in captured.out
