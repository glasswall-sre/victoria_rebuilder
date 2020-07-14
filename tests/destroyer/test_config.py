import pytest

from victoria_rebuilder.config import RebuilderConfig, RebuilderSchema, ReleaseConfig, AccessConfig, AccessSchema, DeploymentConfig, DeploymentSchema


def test_create_deployment_config():

    result_schema = DeploymentSchema().load({
        "releases": [{
            "name": "Platform.test"
        }, {
            "name": "Platform.test2"
        }],
        "stage":
        "test"
    })

    result_object = DeploymentConfig(
        [ReleaseConfig("Platform.test"),
         ReleaseConfig("Platform.test2")], "test")

    assert result_schema == result_object


def test_create_access_config():

    result = AccessSchema().load({
        "access_token": "12344",
        "organisation": "glasswall",
        "project": "Test_project",
        "email": "testemail@email.com"
    })

    assert result == AccessConfig("12344", "glasswall", "Test_project",
                                  "testemail@email.com")


def test_create_destroy_config():

    result = RebuilderSchema().load({
        "access": {
            "access_token": "12344",
            "organisation": "glasswall",
            "project": "Test_project",
            "email": "testemail@email.com"
        },
        "deployments": [{
            "stage":
            "test",
            "releases": [{
                "name": "Platform.test"
            }, {
                "name": "Platform.test2"
            }]
        }]
    })

    assert result == RebuilderConfig(
        AccessConfig("12344", "glasswall", "Test_project",
                     "testemail@email.com"),
        [
            DeploymentConfig([
                ReleaseConfig("Platform.test"),
                ReleaseConfig("Platform.test2")
            ], "test")
        ],
    )
