import pytest

import destroyer
from types import SimpleNamespace
from destroyer import client
from destroyer import config
from destroyer import rebuild
from munch import munchify


class MockReleaseClient:
    def get_releases(self, *args, **kwargs):

        release_list = {
            "value": [{
                "id": 123,
                "release_definition": {
                    "name": "Platform.Infrastructure"
                }
            }]
        }

        return munchify(release_list)

    def get_release(self, *args, **kwargs):

        release = {
            "environments": [{
                "name": "pent",
                "status": "succeeded",
                "id": 321
            }]
        }

        return munchify(release)

    def get_release_environment(self, *args, **kwargs):
        print(args)
        release_environment = {"status": "rejected"}

        return munchify(release_environment)

    def update_release_environment(self, *args, **kwargs):
        return "Done"


class MockClients:
    def get_release_client(self):
        return MockReleaseClient()


class MockBasicAuthentication:
    def __init__(self, *args, **kwargs):
        pass


class MockConnection:
    clients_v5_1 = MockClients()

    def __init__(self, *args, **kwargs):
        pass


class MockConfig:
    project = "mocked_project"
    access_token = "mocked_access_token"
    organisation = "mocked_organisation"


def create_mock_client(monkeypatch):
    monkeypatch.setattr(destroyer.client, "Connection", MockConnection)
    monkeypatch.setattr(destroyer.client, "BasicAuthentication",
                        MockBasicAuthentication)

    return client.Client(MockConfig())


@pytest.fixture
def mock_client(monkeypatch):
    return create_mock_client(monkeypatch)


def create_mock_rebuild(monkeypatch, mock_client):

    monkeypatch.setattr(destroyer.client, "Connection", MockConnection)
    monkeypatch.setattr(destroyer.client, "BasicAuthentication",
                        MockBasicAuthentication)
    # monkeypatch.setattr(destroyer.rebuild, "Client", mock_client)

    destroyer_config = config.load("tests/destroyer/test_config.yaml")

    return rebuild.Rebuild("pent", destroyer_config.access,
                           destroyer_config.deployments)


@pytest.fixture
def mock_rebuild(monkeypatch, mock_client):

    return create_mock_rebuild(monkeypatch, mock_client)
