from click.testing import CliRunner
import pytest
from victoria_destroyer.cli import destroyer
from conftest import create_mock_client


@pytest.fixture
def mock_cli(monkeypatch):
    def create_client(*args, **kwargs):
        return create_mock_client(monkeypatch)
