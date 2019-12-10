import pytest

import destroyer
from types import SimpleNamespace
from destroyer import release


class MockReleaseClient:
    def get_releases(self, *args, **kwargs):
        release_list = SimpleNamespace()
        release_list.value = []
        release = SimpleNamespace()
        release.id = 123
        release_list.value.append(release)

        return release_list

    def get_release(self, *args, **kwargs):
        release = SimpleNamespace()
        environment = SimpleNamespace()
        environment.name = "dev"
        environment.status = "succeeded"
        environment.id = 321
        release.environments = [environment]

        return release


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


def create_mock_client(monkeypatch):
    monkeypatch.setattr(destroyer.release, "Connection", MockConnection)
    monkeypatch.setattr(destroyer.release, "BasicAuthentication",
                        MockBasicAuthentication)

    return release.Release("Platform.Infrastructure", "dev", MockConfig())


@pytest.fixture
def mock_client(monkeypatch):
    return create_mock_client(monkeypatch)