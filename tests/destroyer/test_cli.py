from click.testing import CliRunner
import pytest
from victoria_rebuilder.cli import rebuilder
from conftest import create_mock_client


@pytest.fixture
def mock_cli(monkeypatch):
    def create_client(*args, **kwargs):
        return create_mock_client(monkeypatch)
