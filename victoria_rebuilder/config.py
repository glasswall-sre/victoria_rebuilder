"""config.py

Config defines the config for the Rebuilder and a marshmallow schema for
validating the config.

Author:
    Alex Potter-Dixon <apotter-dixon@glasswallsolutions.com>
"""
import logging.config
from os.path import basename
from typing import Dict, List

import yaml
from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load


class AccessSchema(Schema):
    """Marshmallow schema for the Accessing AzureDevops plugin config."""
    access_token = fields.Str()
    organisation = fields.Str()
    project = fields.Str()
    email = fields.Email()

    @post_load
    def create_access_config(self, data, **kwargs):
        return AccessConfig(**data)


class AccessConfig:
    """AccessConfig is the config for accessing Azure Devops.

    Attributes:
        access_token (str): The access token for the Azure DevOps API.
        organisation (str): The Azure DevOps organisation to use.
        project (str): The Azure DevOps plugin to use.
        email (str): The email the user uses with Azure DevOps.
    """
    def __init__(self, access_token: str, organisation: str, project: str,
                 email: str) -> None:
        self.access_token = access_token
        self.organisation = organisation
        self.project = project
        self.email = email

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.access_token == other.access_token \
                and self.organisation == other.organisation \
                and self.project == other.project \
                and self.email == other.email
        return False


class ReleaseSchema(Schema):
    """Schema for releases"""
    name = fields.Str()

    @post_load
    def create_release_config(self, data, **kwargs):
        return ReleaseConfig(**data)


class ReleaseConfig:
    """ReleaseConfig is the config for releases in Azure Devops.

    Attributes:
        name (str): Name of the release.

    Parameters:
        complete (bool): If a release is complete.
        release_id (int): The release id of the release.
        environment_id (int): The id of the environment associated with the release.
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.complete = False
        self.release_id = 0
        self.environment_id = 0

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.name == other.name
        return False


class DeploymentSchema(Schema):
    """Marshmallow schema for deployments."""
    stage = fields.Str()
    releases = fields.List(fields.Nested(ReleaseSchema))

    @post_load
    def create_deployment_config(self, data, **kwargs):
        return DeploymentConfig(**data)


class DeploymentConfig:
    """StageConfig is the config for stages.

    Attributes:
        releases (List[str]): The list of releases to deploy.


    """
    def __init__(self, releases: List[ReleaseConfig], stage: str) -> None:
        self.releases = releases
        self.stage = stage
        self.complete = False

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.releases == other.releases and self.stage == other.stage
        return False


class RebuilderSchema(Schema):
    """Marshmallow schema for rebuilder."""
    access = fields.Nested(AccessSchema)
    deployments = fields.List(fields.Nested(DeploymentSchema))
    environments = fields.List(fields.Str)

    @post_load
    def make_destoyer_config(self, data, **kwargs):
        """Callback used by marshmallow after loading object. We're using it here
        to create an instance of Config after loading the data."""
        return RebuilderConfig(**data)


class RebuilderConfig:
    """DeploymentConfig is the config for deployments.

    Attributes:
        stages (List[StageConfig}): List of stage configurations.
    """
    def __init__(
            self,
            access: AccessConfig,
            deployments: List[DeploymentConfig],
    ) -> None:

        self.access = access
        self.deployments = deployments

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.access == other.access \
                   and self.deployments == other.deployments
        return False


CONFIG_SCHEMA = RebuilderSchema(unknown=EXCLUDE)
"""Instance of ConfigSchema to use for validation."""
