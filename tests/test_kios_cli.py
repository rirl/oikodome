from datetime import datetime as real_datetime
from kios import cli
class FixedDateTime:
    @staticmethod
    def now():
        return real_datetime(2020, 1, 2, 3, 4, 5)


def test_slugify():
    assert cli.slugify("Hello World") == "hello-world"
    assert cli.slugify(" A/B C ") == "a-b-c"
    assert cli.slugify("MixedCASE") == "mixedcase"


def test_investigate_creates_structure(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(cli, 'INVESTIGATIONS_DIR', tmp_path / "investigations")
    monkeypatch.setattr(cli, 'datetime', FixedDateTime)
    topic = "My Topic"
    cli.investigate(topic)
    captured = capsys.readouterr()

    ts = FixedDateTime.now().strftime("%Y%m%d-%H%M%S")
    inv_id = f"INV-{ts}"
    slug = cli.slugify(topic)
    path = tmp_path / "investigations" / f"{inv_id}-{slug}"

    assert (path / "prompts").is_dir()
    assert (path / "responses").is_dir()
    assert (path / "investigation.adoc").is_file()

    content = (path / "investigation.adoc").read_text()
    assert f"ID:: {inv_id}" in content
    assert f"Title:: {topic}" in content
    assert "Created::" in content
    assert f"Created: {inv_id}" in captured.out

def test_status_reports_investigations(tmp_path, monkeypatch, capsys):
    base = tmp_path / "investigations"
    base.mkdir()
    (base / "INV-1-topic-a").mkdir()
    (base / "INV-2-topic-b").mkdir()
    monkeypatch.setattr(cli, 'INVESTIGATIONS_DIR', base)

    cli.status()
    captured = capsys.readouterr()
    assert "Investigations: 2" in captured.out
    assert "INV-1-topic-a" in captured.out
    assert "INV-2-topic-b" in captured.out
