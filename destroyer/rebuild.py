"""
Runs and holds the states of deployments for a particular environment.

Parameters:
    environment (str): The environment to rebuild.
    access_cfg (AccessConfig): The configuration to access AzureDevOps.
    deployments (DeploymentConfig): The configuration to process the deployments.

"""
import time
import logging
import copy
import pickle
import os
from typing import List, Union

from destroyer.config import AccessConfig, DeploymentConfig
from destroyer.release import Release
from destroyer.client import Client

STATE_FILE = "rebuild"


class Rebuild:
    def __init__(self, environment: str, access_cfg: AccessConfig,
                 ***REMOVED*** DeploymentConfig):

        self.deployments = deployments
        self.environment = environment
        self.access_cfg = access_cfg
        self.deployments = deployments
        self._load()
        self.client = Client(access_cfg)

    def run_deployments(self):
        """
        Rebuilds the environment by running group of deployments.
        Once a deployment has been completed the next one is run.
        """
        for deployment in self.***REMOVED***

            if not deployment.complete:
                logging.info(f"Running deployment {deployment.stage}")
                self.run_releases(deployment.releases, self.environment,
                                  self.access_cfg)
                self.wait_to_complete(deployment.releases, 10)
                deployment.complete = True
                self._save()

            logging.info(f"Deployment {deployment.stage} has completed.")
        self._clean_up()

    def run_releases(self, releases: List[str], environment: str,
                     ***REMOVED*** AccessConfig) -> None:
        """
        Runs a list of releases associated to a specific deployment and environment.

        Arguments:
            releases (List[str]): List of releases that need running.
            environment (str): The environment to run the releases on.
            access (AccessConfig): The configuration to login into Azure DevOps.

        """
        for release in releases:
            if not release.complete:
                release.release_id, release.environment_id = self.client.get_latest_release(
                    release.name, environment)

                self.client.run_release(release.release_id,
                                        release.environment_id)

    def wait_to_complete(self, releases: List[Release], interval):
        """
        Waits for the releases to complete. Loops until
        """

        running = True

        while running:
            time.sleep(interval)
            running = False
            for release in releases:
                if not release.complete:
                    release.complete = self.client.is_release_complete(
                        release.release_id, release.environment_id)
                    if not release.complete: running = True
                else:
                    self._save()

    def _load(self):
        try:
            with open(STATE_FILE, 'rb') as rebuild_obj_file:
                loaded_dict = pickle.load(rebuild_obj_file)
                self.__dict__.update(loaded_dict)
        except IOError:
            print(f"Unable to find rebuild file. Assuming fresh run. ")

    def _save(self):
        with open(STATE_FILE, 'wb') as rebuild_obj_file:
            current_state = copy.copy(self.__dict__)

            current_state['client'] = None

            pickle.dump(current_state, rebuild_obj_file)

    def _clean_up(self):
        os.remove(STATE_FILE)
