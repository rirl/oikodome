from kios.cli import create_investigation, slugify


def test_slugify() -> None:
    assert slugify("What is Embodied Cognition?") == "what-is-embodied-cognition"


def test_create_investigation(tmp_path) -> None:
    path = create_investigation("test investigation", root=tmp_path)

    assert path.exists()
    assert (path / "metadata.yaml").exists()
    assert (path / "prompt.adoc").exists()
    assert (path / "research-log.adoc").exists()
    assert (path / "report.adoc").exists()
