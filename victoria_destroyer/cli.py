"""cli.py

This is the module that contains the Click CLI for the Destroyer

Author:
    Alex Potter-Dixon <apotter-dixon@glasswallsolutions.com>
"""

import click
import logging
from typing import List, Union

from .config import DestroyerConfig
from .rebuild import Rebuild


@click.group()
@click.pass_obj
def destroyer(cfg: DestroyerConfig):
    """
    The Destroyer allows the destruction and rebuilding of environments via CLI. 
    """
    pass


@destroyer.command()
@click.argument('from_env', nargs=1, type=str)
@click.argument('to_env', nargs=-1, type=str)
@click.pass_obj
def copy(cfg: DestroyerConfig, from_env: str, to_env: str) -> None:
    """
    CLI call for rebuilding a list of environments based off
    a single environment
    Arguments:
        from_env (str): The environment to rebuild from in Azure DevOps.
        to_env (List[str]): The list of environments to rebuild

    """
    logging.info(
        f"Rebuilding environments {from_env} from environment: {to_env}")

    for env in to_env:
        logging.info(f"Rebuilding environment {env} ")
        env_rebuild = Rebuild(
            env,
            cfg.access,
            cfg.deployments,
        )

        #  env_rebuild.run_deployments()

        logging.info(f"Successfully built {env}")

    logging.info(f"Fully rebuilt all environments: {to_env}")


@destroyer.command()
@click.argument('env', nargs=1, type=str)
@click.pass_obj
def rebuild(cfg: DestroyerConfig, env: str) -> None:
    """
    CLI call for rebuilding a specific kubernetes environment
    Arguments:
        cfg (str): The destroyer config.
        env (str): Environment to rebuild.  
    """

    logging.info(f"Rebuilding environment {env} ")
    env_rebuild = Rebuild(
        env,
        cfg.access,
        cfg.deployments,
    )

    env_rebuild.run_deployments()

    logging.info(f"Successfully built {env}")
