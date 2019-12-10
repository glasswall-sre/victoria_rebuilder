from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from destroyer.config import AccessConfig
from typing import Tuple


class Release:
    """A release in AzureDevOps.

    Parameters:
        name (str): Name of the release pipeline in Azure DevOps.
        environment (str): The environment the release is to be associated with.
        access_cfg (AccessConfig): Configuration to log into AzureDevops with.
       
    """
    def __init__(self, name: str, environment: str, access_cfg: AccessConfig):
        self.name = name
        self.environment = environment
        self.access_cfg = access_cfg
        self.release_client = self.get_release_client()

        self.result = self.get_latest_release()

    def get_latest_release(self) -> Tuple[int, int]:
        """
        Retrieves the latest release and environment id for a specific environment.
        Gets a list of all the releases for a specific release pipeline, loops
        through them and for each release looks for a matching environment and status.        

        Returns:
            The ID of the release and environment that was either succeeded or partially succeeded.

        """

        releases = self.release_client.get_releases(
            self.access_cfg.project, search_text=self.name).value
        for release in releases:
            result = self.release_client.get_release(self.access_cfg.project,
                                                     release_id=release.id)

            for environment in result.environments:
                if environment.name == self.environment and (
                        environment.status == "succeeded"
                        or environment.status == "partiallySucceeded"):
                    return release.id, environment.id

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

        return connection.clients.get_release_client()
