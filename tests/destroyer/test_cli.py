from click.testing import CliRunner
import pytest
from destroyer.cli import destroyer
from conftest import create_mock_client


@pytest.fixture
def mock_cli(monkeypatch):
    def create_client(*args, **kwargs):
        return create_mock_client(monkeypatch)


def test_destroyer_cli_rebuild(mock_cli):
    """Test to see if we can get a work item."""
    runner = CliRunner()
    result = runner.invoke(destroyer, ["rebuild"])
    assert result.exit_code == 0