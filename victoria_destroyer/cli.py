"""cli.py

This is the module that contains the Click CLI for the Destroyer

Author:
    Alex Potter-Dixon <apotter-dixon@glasswallsolutions.com>
"""

import click
import logging

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
@click.option('--env',
              required=True,
              type=str,
              prompt="Environment",
              help="Environment you want to rebuild.")
@click.pass_obj
def rebuild(cfg: DestroyerConfig, env: str) -> None:
    """
    CLI call for rebuilding a specific kubernetes environment
    Arguments:
        cfg (str): Path to the config file.
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
