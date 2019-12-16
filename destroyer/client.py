from typing import Tuple

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

from destroyer.config import AccessConfig
import logging
import sys


class Client:
    def __init__(self, access_cfg: AccessConfig):

        self.access_cfg = access_cfg
        self.release_client = self.get_release_client()

    def is_release_complete(self, release_id, environment_id, name):
        """
        Checks to see if a release has finished running for a specific environment.
        Returns:
            The status of the release. Can be succeeded, partiallySucceeded or failed.
        """
        release_environment = self.release_client.get_release_environment(
            self.access_cfg.project,
            release_id=release_id,
            environment_id=environment_id)

        if release_environment.status == "rejected" or release_environment.status == "cancelled":
            logging.critical(
                f"Release {name} has failed to deploy. The status is {release_environment.status}"
            )
            sys.exit(1)

        return release_environment.status == "succeeded" or release_environment.status == "partiallySucceeded"

    def get_latest_release(self, name: str, env_name: str) -> Tuple[int, int]:
        """
        Retrieves the latest release and environment id for a specific environment.
        Gets a list of all the releases for a specific release pipeline, loops
        through them and for each release looks for a matching environment and status.

        Arguments:
            name: (str) Name of the release pipeline.
            env_name (str): Name of the environment that the release was run.

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
                print(release.release_definition.name)
                for environment in result.environments:

                    if environment.name == env_name and (
                            environment.status == "succeeded"
                            or environment.status == "partiallySucceeded"):
                        logging.info(
                            f"Found environment for {name} with id: {environment.id} "
                        )
                        return release.id, environment.id

        return None, None

    def run_release(self, release_id, environment_id):
        """
        Runs the latest succeeded or partically succeeded pipeline associated
        with the object.

        """

        start_values = {
            "comment": "Run by the DESTROYER",
            "status": "inProgress"
        }

        self.release_client.update_release_environment(start_values,
                                                       self.access_cfg.project,
                                                       release_id,
                                                       environment_id)

    def get_release_client(self):
        """
        Logins to the Azure DevOps API and gets the release client.

        Returns:
            The Release client of the Azure DevOps API.
        """
        credentials = BasicAuthentication("", self.access_cfg.access_token)
        connection = Connection(
            base_url=f"https://dev.azure.com/{self.access_cfg.organisation}/",
            creds=credentials)

        return connection.clients_v5_1.get_release_client()
