"""
Runs and holds the states of deployments for a particular environment.

Parameters:
    from_environment (str): The environment to rebuild from.
    to_environment (str): The environment to rebuild.
    access_cfg (AccessConfig): The configuration to access AzureDevOps.
    deployments (DeploymentConfig): The configuration to process the deployments.
    fresh (bool): If the rebuilder should use the previous state file.

"""
import time
import logging
import copy
import pickle
import os
import sys
from typing import List, Union

from victoria_rebuilder.config import AccessConfig, DeploymentConfig, ReleaseConfig
from victoria_rebuilder.client import DevOpsClient

# The location of the state file.
STATE_FILE = "rebuild"


class Rebuild:
    def __init__(self, from_environment: str, target_environment: str,
                 access_cfg: AccessConfig, deployments: DeploymentConfig,
                 resume):

        self.deployments = deployments
        self.from_environment = from_environment
        self.target_environment = target_environment
        self.access_cfg = access_cfg
        self.deployments = deployments
        self._load(resume)
        self.client = DevOpsClient(access_cfg)

    def run_deployments(self):
        """
        Rebuilds the environment by running group of deployments.
        Once a deployment has been completed its state is saved and
        the next deployment is run.
        """
        for deployment in self.deployments:

            if not deployment.complete:
                logging.info(f"Running deployment {deployment.stage}")

                deployment.releases = self.run_releases(
                    deployment.releases, self.from_environment,
                    self.target_environment)
                deployment.releases = self.wait_to_complete(
                    deployment.releases, 10)
                deployment.complete = True
                self._save()

            logging.info(f"Deployment {deployment.stage} has completed.")
        self._clean_up()

    def run_releases(self, releases: List[str], from_environment: str,
                     target_environment: str) -> List[ReleaseConfig]:
        """
        Runs a list of releases associated to a specific deployment and environment.
        If it can't find the release it assumes its not available for that environment
        so it is removed from the list.

        Arguments:
            releases (List[str]): List of releases that need running.
            target_environment (str): The environment to run the release on.
            from_environment (str): The environment you want to base the target environment on.

        Returns:
            A list of Releases (ReleaseConfig). Releases that weren't found would of been removed.
        """
        for release in releases[:]:

            if not release.complete:

                if not release.release_id:
                    release.release_id, release.environment_id = self.client.get_latest_successful_release(
                        release.name, from_environment, target_environment)

                if release.release_id and release.environment_id:
                    self.client.run_release(release.release_id,
                                            release.environment_id, release.name)

                else:
                    logging.info(
                        f"Unable to run release for {release.name}. Either no environment for release or it is currently running."
                    )
                    releases.remove(release)

            self._save()

        return releases

    def wait_to_complete(self, releases: List[ReleaseConfig],
                         interval: int) -> List[ReleaseConfig]:
        """
        Waits for the releases to complete.

        Arguments:
            releases (list[ReleaseConfig]): The list of releases to wait for.
            interval (int): In seconds how often to check if the release is complete.

        Returns:
            A list of releases (ReleaseConfig)
            Once all the releases are complete it returns the list of releases.

        """

        running = True

        while running:

            running = False
            for release in releases:
                time.sleep(interval)

                if not release.complete:
                    release_status = self.client.get_release_status(
                        release.release_id, release.environment_id,
                        release.name)
                    if release_status == "succeeded" or release_status == "partiallySucceeded":
                        logging.info(f"{release.name} is complete.")
                        release.complete = True
                        self._save()
                    elif release_status == "rejected" or release_status == "cancelled":
                        re_run_release = self._re_run_failed_release(release.release_id, release.environment_id, release.name)       
                        release.complete = False if re_run_release else True                   
                    else:
                        running = True                   

        return releases

    def _re_run_failed_release(self, release_id: int, release_env_id: int, release_name: str)-> bool:
        """
        Asks the user if they want to re run a failed release.

        Arguments:
            release_id (int): The release pipeline ID in Azure DevOpS.
            release_env_id (int): The particular stage ID in Azure DevOps.
            release_name (str): The name of the release pipeline.

        Returns:
            If the user decided to run the pipeline again.
        """
        logging.info(f"{release_name} has not been successful.")

        run_again = self._query_yes_no(f"Would you like to run {release_name} again?")

        if run_again:
            self.client.run_release(release_id, release_env_id, release_name)
        else:
            logging.info(f"{release_name} will not be run again. Continuing with the deployment.")
        
        return run_again

        
    
    def _query_yes_no(self, question: str, default="yes") -> bool:
        """
        Ask a yes/no question via input() and return their answer.

        Arguments:
            question (str): A string that is presented to the user.
            default (str): The presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        Returns:
            The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True,
                "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                "(or 'y' or 'n').\n")
        

    def _load(self, resume:bool) -> None:
        """
        Loads the pickled file of the current object and de-serializes so it can resume
        if there's been a crash or an issue with the pipeline.

        resume (bool): If the rebuilder should use the previous state file.
        """
        if resume:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, 'rb') as rebuild_obj_file:
                    # nosec
                    loaded_dict = pickle.load(rebuild_obj_file)
                    self.__dict__.update(loaded_dict)
            else:
                logging.info(
                    f"Unable to find rebuild file. Assuming fresh run. ")
        else:
            self._clean_up()
            logging.info(f"Fresh run so have removed the previous state file.")

    def _save(self)-> None:
        """
        Creates a deep copy of the current state of the object, removes the client
        connection so it can be pickled, pickles self and saves it to a file.
        """
        with open(STATE_FILE, 'wb') as rebuild_obj_file:
            current_state = copy.copy(self.__dict__)

            current_state['client'] = None

            pickle.dump(current_state, rebuild_obj_file)

    def _clean_up(self) -> None:
        """
        If the deployment has been successful then the state file
        is removed.
        """
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
