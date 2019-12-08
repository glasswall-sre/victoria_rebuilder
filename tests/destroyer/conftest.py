import pytest

import destroyer
from destroyer import release


class MockReleaseClient:
    def get_releases(self):
        return [{}]


class MockClients:
    def get_release_client(self):
        return MockReleaseClient()


class MockBasicAuthentication:
    def __init__(self, *args, **kwargs):
        pass


class MockConnection:
    clients = MockClients()

    def __init__(self, *args, **kwargs):
        pass


class MockConfig:
    project = "mocked_project"
    access_token = "mocked_access_token"
    organisation = "mocked_organisation"


def create_mock_api(monkeypatch):
    monkeypatch.setattr(destroyer.release, "Connection", MockConnection)
    monkeypatch.setattr(destroyer.release, "BasicAuthentication",
                        MockBasicAuthentication)

    return release.Release("Platform.Infrastructure", "dev", MockConfig())


@pytest.fixture
def mock_api(monkeypatch):
    return create_mock_api(monkeypatch)