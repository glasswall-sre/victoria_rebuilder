from destroyer.release import Release
from destroyer.config import AccessConfig, DeploymentConfig
from typing import Union, List


def rebuild_environment(environment: str, access: AccessConfig,
                        deployments: DeploymentConfig) -> None:
    """
    Rebuilds the environment by running group of deployments.
    Once a deployment has been completed the next one is run.

    Arguments:
        environment (str): The environment to rebuild.
        access (AccessConfig): The configuration to access AzureDevOps.
        deployments (DeploymentConfig): The configuration to process the deployments.

    """

    for deployment in deployments:
        run_pipelines(deployment.pipelines, environment, access)


def run_pipelines(pipelines: List[str], environment: str,
                  access: AccessConfig) -> None:
    """
    Runs a list of pipelines associated to a specific deployment and environment.

    Arguments:
        pipelines (List[str]): List of pipelines that need running.
        environment (str): The environment to run the pipelines on.
        access (AccessConfig): The configuration to login into Azure DevOps.

    """

    releases = []

    for pipeline in pipelines:
        release = Release(pipeline, environment, access)
        releases.append(release)
