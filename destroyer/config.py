"""config.py

Config defines the config for the Destroyer and a marshmallow schema for
validating the config.

Author:
    Alex Potter-Dixon <apotter-dixon@glasswallsolutions.com>
"""
import logging
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


class StageSchema(Schema):
    """Marshmallow schema for Stage schema."""
    pipelines = fields.List(fields.Str)
    dependsOn = fields.Str()

    @post_load
    def create_stage_config(self, data, **kwargs):
        return StageConfig(**data)


class StageConfig:
    """StageConfig is the config for stages.

    Attributes:
        pipelines (List[str]): The list of pipelines to deploy
      
    """
    def __init__(self, pipelines: List[str], dependsOn: str) -> None:
        self.pipelines = pipelines
        self.depends_on = dependsOn

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.pipelines == other.pipelines \
                and self.depends_on == other.depends_on


class DeploymentSchema(Schema):
    """Marshmallow schema for deployments."""

    stage = fields.Str()
    pipelines = fields.List(fields.Str())

    @post_load
    def create_deployment_config(self, data, **kwargs):
        return DeploymentConfig(**data)


class DeploymentConfig:
    """StageConfig is the config for stages.

    Attributes:
        pipelines (List[str]): The list of pipelines to deploy.
      
      
    """
    def __init__(self, pipelines: List[str], stage: str) -> None:
        self.pipelines = pipelines
        self.stage = stage

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.pipelines == other.pipelines and self.stage == other.stage


class DestroyerSchema(Schema):
    """Mashmallow schema for destroyer."""
    access = fields.Nested(AccessSchema)
    deployments = fields.List(fields.Nested(DeploymentSchema))
    environments = fields.List(fields.Str)

    @post_load
    def make_destoyer_config(self, data, **kwargs):
        """Callback used by marshmallow after loading object. We're using it here
        to create an instance of Config after loading the data."""
        return DestroyerConfig(**data)


class DestroyerConfig:
    """DeploymentConfig is the config for deployments.

    Attributes:
        stages (List[StageConfig}): List of stage configurations.
    """
    def __init__(self, ***REMOVED*** AccessConfig, ***REMOVED*** List[StageConfig],
                 environments: List[str]) -> None:
        self.access = access
        self.deployments = deployments
        self.environments = environments

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.access == other.access \
                   and self.deployments == other.deployments \
                   and self.environments == other.environments


CONFIG_SCHEMA = DestroyerSchema(unknown=EXCLUDE)
"""Instance of ConfigSchema to use for validation."""


def __print_validation_err(err: ValidationError, name: str) -> None:
    """Internal function used for logging a validation error in the Schema.

    Args:
        err (ValidationError): The error to log.
        name (str): A human-readable identifier for the Schema data source. Like a filename.
    """
    # build up a string for each error
    log_str = []
    log_str.append(f"Error loading file '{name}':")
    for field_name, err_msgs in err.messages.items():
        log_str.append(f"{field_name}: {err_msgs}")

    # log the joined up string, and exit with an error
    logging.critical(" ".join(log_str))
    raise SystemExit(1)


def load(config_file_path: str) -> DeploymentConfig:
    """Load a config file from a given path."""
    logging.info(f"Loading config file '{basename(config_file_path)}'")
    with open(config_file_path, "r") as config_file:
        raw_config = yaml.safe_load(config_file)
        try:

            loaded_config = CONFIG_SCHEMA.load(raw_config)
            return loaded_config
        except ValidationError as err:
            # print any errors if there are any
            __print_validation_err(err, basename(config_file_path))
