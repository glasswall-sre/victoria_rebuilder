import pytest

from tests.rebuilder.conftest import create_mock_client


@pytest.fixture
def mock_cli(monkeypatch):
    def create_client(*args, **kwargs):
        return create_mock_client(monkeypatch)
