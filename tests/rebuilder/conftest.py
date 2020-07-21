import pytest

import victoria_rebuilder
from types import SimpleNamespace
from victoria_rebuilder import client
from victoria_rebuilder import config
from victoria_rebuilder.rebuild import Rebuild
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
            },{
                "name": "stage",
                "status": "rejected",
                "id": 322
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
        elif environment_id == 1:
            release_environment = {"status": "inProgress"}

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
    monkeypatch.setattr(victoria_rebuilder.client, "Connection",
                        MockConnection)
    monkeypatch.setattr(victoria_rebuilder.client, "BasicAuthentication",
                        MockBasicAuthentication)

    return client.DevOpsClient(MockConfig())


@pytest.fixture
def mock_client(monkeypatch):
    return create_mock_client(monkeypatch)


def create_mock_rebuild(monkeypatch, mock_client):

    monkeypatch.setattr(victoria_rebuilder.client, "Connection",
                        MockConnection)
    monkeypatch.setattr(victoria_rebuilder.client, "BasicAuthentication",
                        MockBasicAuthentication)

    rebuilder_config = config.RebuilderSchema().load({
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

    return Rebuild("qa", "pent", rebuilder_config.access,
                   rebuilder_config.deployments, False)


@pytest.fixture
def mock_rebuild(monkeypatch, mock_client):

    return create_mock_rebuild(monkeypatch, mock_client)
