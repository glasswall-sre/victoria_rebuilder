import pytest

import victoria_destroyer
from types import SimpleNamespace
from victoria_destroyer import client
from victoria_destroyer import config
from victoria_destroyer.rebuild import Rebuild
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
            }, {
                "name": "qa",
                "status": "succeeded",
                "id": 456
            }]
        }

        return munchify(release)

    def get_release_environment(self, project, release_id, environment_id):
        release_environment = {}
        if environment_id == 321:
            release_environment = {"status": "rejected"}
        elif environment_id == 432:
            release_environment = {"status": "succeeded"}

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
    monkeypatch.setattr(victoria_destroyer.client, "Connection",
                        MockConnection)
    monkeypatch.setattr(victoria_destroyer.client, "BasicAuthentication",
                        MockBasicAuthentication)

    return client.DevOpsClient(MockConfig())


@pytest.fixture
def mock_client(monkeypatch):
    return create_mock_client(monkeypatch)


def create_mock_rebuild(monkeypatch, mock_client):

    monkeypatch.setattr(victoria_destroyer.client, "Connection",
                        MockConnection)
    monkeypatch.setattr(victoria_destroyer.client, "BasicAuthentication",
                        MockBasicAuthentication)

    destroyer_config = config.DestroyerSchema().load({
        "access": {
            "access_token": "12344",
            "organisation": "glasswall",
            "project": "Test_project",
            "email": "testemail@email.com"
        },
        "deployments": [{
            "stage":
            "pent",
            "releases": [{
                "name": "Platform.Infrastructure"
            }, {
                "name": "Platform.test2"
            }]
        }]
    })

    return Rebuild("qa", "pent", destroyer_config.access,
                   destroyer_config.deployments, False)


@pytest.fixture
def mock_rebuild(monkeypatch, mock_client):

    return create_mock_rebuild(monkeypatch, mock_client)
