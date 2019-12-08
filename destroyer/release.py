from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from config import AccessConfig


class Release:
    def __init__(self, name, environment, access_cfg):
        self.name = name
        self.access_cfg = access_cfg
        self.release_api = self.ReleaseAPI(access_cfg)
        self.latest_release = self.get_latest_release("success")

    def get_latest_release(self, status):
        """
        Retrieves the latest release that has been run.
        
        Attributes:
            status (str): If successful, failed or abandoned.

        Returns:
            The ID of the release

        """

        result = self.release_api.get_releases(self.name)
        print(result)

    class ReleaseAPI:
        """A connection to the Release Azure DevOps API.

        Parameters:
            credentials (BasicAuthentication): The credentials used to connect.
            connection (Connection): The actual connection to the API.
            work_item_client (WorkItemTrackingClient): A client for work item tracking.
            work_client (WorkClient): A client for work tracking.
        """
        def __init__(self, cfg: AccessConfig) -> None:
            """Connect to the Azure DevOps API using the PBI config.

            Args:
                project (str): The Azure DevOps project to use.
                cfg (PBIConfig): The config to use to connect to the API.
            """
            self.project = cfg.project
            self._connect(cfg.access_token, cfg.organisation)
           
        def _connect(self, access_token: str, organisation: str):
            """Connect to the Azure DevOps API.

            Args:
                access_token (str): The access token to authenticate with.
                organisation (str): The Azure DevOps organisation to use.
            """
            self.credentials = BasicAuthentication("", access_token)
            self.connection = Connection(
                base_url=f"https://dev.azure.com/{organisation}/",
                creds=self.credentials)
            self.release_client = self.connection.clients.get_release_client()


        def get_releases(self, name):
            print(name)
            result = self.release_client.get_releases(self.project,
                                                      search_text=name).value

            return result
