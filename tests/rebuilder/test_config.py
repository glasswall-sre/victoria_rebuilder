from victoria.encryption.schemas import EncryptionEnvelope

from victoria_rebuilder.config import RebuilderConfig, RebuilderSchema, ReleaseConfig, AccessSchema, \
    DeploymentConfig, DeploymentSchema, EncryptedAccessConfig


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


def test_create_access_config(mock_access_data):
    result = AccessSchema().load(mock_access_data)

    assert result == EncryptedAccessConfig(access_token=EncryptionEnvelope(**mock_access_data["access_token"]),
                                           organisation=mock_access_data["organisation"],
                                           project=mock_access_data["project"],
                                           email=mock_access_data["email"])


def test_create_destroy_config(mock_access_data):
    result = RebuilderSchema().load({
        "access": mock_access_data,
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
        EncryptedAccessConfig(access_token=EncryptionEnvelope(**mock_access_data["access_token"]),
                              organisation=mock_access_data["organisation"],
                              project=mock_access_data["project"],
                              email=mock_access_data["email"]),
        [
            DeploymentConfig([
                ReleaseConfig("Platform.test"),
                ReleaseConfig("Platform.test2")
            ], "test")
        ],
    )
