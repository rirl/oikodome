import io
import sys
from kios import cli

def test_version_output(capsys):
    rc = cli.main(["--version"])
    captured = capsys.readouterr()
    assert rc == 0
    assert "KIOS MVP v2" in captured.out
