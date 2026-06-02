from kios import cli

def test_module_exports():
    # Ensure the CLI module exposes the expected Typer app and commands
    assert hasattr(cli, "app")
    assert hasattr(cli, "investigate")
    assert hasattr(cli, "status")
    assert hasattr(cli, "slugify")
