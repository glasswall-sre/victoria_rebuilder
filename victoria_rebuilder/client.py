"""
A further wrapper on the AzureDevops Python API to abstract commmon interactions
with Azure Devops such as checking if a release is complete.

Parameters:
    access_cfg (AccessConfig): The configuration to access AzureDevOps.

"""

from typing import Tuple, Union

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

from victoria_rebuilder.config import AccessConfig
import logging
import sys


class DevOpsClient:
    def __init__(self, access_cfg: AccessConfig):

        self.access_cfg = access_cfg
        self._connect()

    def get_release_status(self, release_id: str, environment_id: int,
                            name: str) -> bool:
        """
        Retrieves the current release status of a particular release and environment.

        Arguments:
            release_id (int): ID of the release in Azure DevOps.
            environment_id (int): ID of the environment in a specific release.
            name (str): Name of the release.

        Returns:
            Any of the following results from the Azure DevOps Python SDK:

            canceled: Environment is in canceled state.
            inProgress: Environment is in progress state.
            notStarted: Environment is in not started state.
            partiallySucceeded: Environment is in partially succeeded state.
            queued: Environment is in queued state.
            rejected: Environment is in rejected state.
            scheduled: Environment is in scheduled state.
            succeeded: Environment is in succeeded state.
            undefined:Environment status not set.

        """
        print(self.access_cfg.project)
        print(release_id)
        print(environment_id)
        release_environment = self.release_client.get_release_environment(
            self.access_cfg.project,
            release_id=release_id,
            environment_id=environment_id)

        return release_environment.status

    def get_latest_successful_release(
            self, name: str, from_env: str,
            target_env: str) -> Union[Tuple[None, None], Tuple[int, int]]:
        """
        Gets the release and environment id for a target environment based off a base environments most
        recent successful or partially successful release.
        Gets a list of all the releases for a specific release pipeline, loops
        through them and for each release looks for a matching environment and status.

        Arguments:
            name: (str) Name of the release pipeline.
            from_env (str): Name of the environment you want the target environment to match.
            target_env (str): Name of the environment that you want the release to run on.

        Returns:
            The ID of the release and environment that was either succeeded or partially succeeded.
            If nothing is found then None, None is returned

        """

        releases = self.release_client.get_releases(self.access_cfg.project,
                                                    search_text=name,
                                                    top=200).value

        for release in releases:

            if release.release_definition.name == name:

                result = self.release_client.get_release(
                    self.access_cfg.project, release_id=release.id)

                target_env_id = self._get_target_environment_id(
                    result.environments, target_env)

                for environment in result.environments:
                    
                    if environment.name == from_env and (
                            environment.status == "succeeded"
                            or environment.status == "partiallySucceeded"
                            or environment.status == "queued"
                            or environment.status == "inProgress" ):
                        logging.info(
                            f"Found environment for {name} with id: {environment.id} "
                        )
                        
                        return release.id, target_env_id

        return None, None

    def _get_target_environment_id(self, environments,
                                   environment_name) -> Union[None, int]:
        """
        Internal function used to retrieve the environment id of the target
        environment we want to run a release on.

        Checks to see if InProgress in case the command is run several times by
        mistake.

        environments (List[ReleaseEnvironment]): List of environments to search through.
        environment_name (str): The name of the environment to search for.

        Returns:
            The id of the environment if found. If not found then None is returned.
        """

        for environment in environments:

            if environment.name == environment_name and "inProgress" not in environment.status:
                return environment.id

        return None

    def run_release(self, release_id: int, environment_id: int, release_name: str) -> None:
        """
        Runs the latest succeeded or partically succeeded pipeline associated
        with the object.

        Arguments:
            release_id (int): Id of the release in Azure DevOps.
            environment_id (int): Id of the environment associated to a specific release.
            release_name (str): Name of the release for better logging.

        """
        release_environment = self.release_client.get_release_environment(
            self.access_cfg.project,
            release_id=release_id,
            environment_id=environment_id)

        if release_environment.status != "inProgress" and release_environment.status != "queued":
            start_values = {
                "comment": "Run by Victoria Rebuilder",
                "status": "inProgress"
            }
            self.release_client.update_release_environment(start_values,
                                                            self.access_cfg.project,
                                                            release_id,
                                                            environment_id)
            logging.info(f"Running release {release_id} for {release_name}.")
        else:
            logging.info(f"Release {release_id} for {release_name} is currently {release_environment.status} so not starting for this run.")

    def _connect(self):
        """
        Logins to the Azure DevOps API and sets the release_client.

        """
        credentials = BasicAuthentication("", self.access_cfg.access_token)
        connection = Connection(
            base_url=f"https://dev.azure.com/{self.access_cfg.organisation}/",
            creds=credentials)

        self.release_client = connection.clients_v5_1.get_release_client()
