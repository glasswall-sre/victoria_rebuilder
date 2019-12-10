import pytest

from destroyer.config import DestroyerConfig, DestroyerSchema, AccessConfig, AccessSchema, DeploymentConfig, DeploymentSchema


def test_create_deployment_config():

    result = DeploymentSchema().load({
        "pipelines": ["Platform.test", "Platform.test2"],
        "stage":
        "test"
    })

    assert result == DeploymentConfig(["Platform.test", "Platform.test2"],
                                      "test")


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

    result = DestroyerSchema().load({
        "access": {
            "access_token": "12344",
            "organisation": "glasswall",
            "project": "Test_project",
            "email": "testemail@email.com"
        },
        "deployments": [{
            "stage": "test",
            "pipelines": ["Platform.test", "Platform.test2"]
        }],
        "environments": ["dev", "qa", "pent", "perf"]
    })

    print(result.access.email)

    assert result == DestroyerConfig(
        AccessConfig("12344", "glasswall", "Test_project",
                     "testemail@email.com"),
        [DeploymentConfig(["Platform.test", "Platform.test2"], "test")],
        ["dev", "qa", "pent", "perf"])
