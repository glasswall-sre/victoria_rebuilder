import time
from typing import List, Union

from destroyer.config import AccessConfig, DeploymentConfig
from destroyer.release import Release
from destroyer.planner import Planner


def rebuild_environment(environment: str, ***REMOVED*** AccessConfig,
                        ***REMOVED*** DeploymentConfig) -> None:
    """
    Rebuilds the environment by running group of deployments.
    Once a deployment has been completed the next one is run.

    Arguments:
        environment (str): The environment to rebuild.
        access (AccessConfig): The configuration to access AzureDevOps.
        deployments (DeploymentConfig): The configuration to process the deployments.

    """

    planner = Planner(deployments)

    for deployment in ***REMOVED***
        releases = run_pipelines(deployment.pipelines, environment, access)
        wait_to_complete(releases, 10, 2)


def wait_to_complete(releases: List[Release], timeout, interval):
    """
    Waits for the releases to complete. Loops until 
    """

    timeout_start = time.time()

    while time.time() < timeout_start + timeout:
        time.sleep(interval)
        release_complete = map(lambda releases: releases.is_release_complete())


def run_pipelines(pipelines: List[str], environment: str,
                  ***REMOVED*** AccessConfig) -> None:
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
        release.run_latest_release()
        releases.append(release)

    return releases
