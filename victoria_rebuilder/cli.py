"""cli.py

This is the module that contains the Click CLI for V.I.C.T.O.R.I.A rebuilder

Author:
    Alex Potter-Dixon <apotter-dixon@glasswallsolutions.com>
"""

import click
import logging
from typing import List, Union

from .config import RebuilderConfig
from .rebuild import Rebuild


@click.group()
@click.pass_obj
def rebuilder(cfg: RebuilderConfig):
    """
    The Rebuilder allows the rebuilding of environments via CLI.
    """
    pass


@rebuilder.command()
@click.argument('from_env', nargs=1, type=str)
@click.argument('to_env', nargs=1, type=str)
@click.option(
    '-r',
    '--resume',
    is_flag=True,
    help="If you want the rebuilder to use the previous state file.")
@click.pass_obj
def copy(cfg: RebuilderConfig, from_env: str, to_env: str,
         resume: bool) -> None:
    """
    CLI call for rebuilding an environment based off another environment.
    Arguments:
        from_env (str): The environment to rebuild from in Azure DevOps.
        to_env (str): The environment to rebuild.
        resume (bool): If the rebuilder should resume using previous state file.

    """
    logging.info(
        f"Rebuilding environments {from_env} from environment: {to_env}")

    logging.info(f"Rebuilding environment {to_env}.")
    env_rebuild = Rebuild(from_env.lower(), to_env.lower(), cfg.access,
                          cfg.deployments, resume)

    env_rebuild.run_deployments()

    logging.info(f"Finished running deployments to {to_env}.")


@rebuilder.command()
@click.argument('env', nargs=1, type=str)
@click.option(
    '-r',
    '--resume',
    is_flag=True,
    help="If you don't want the rebuilder to use the previous state file.")
@click.pass_obj
def rebuild(cfg: RebuilderConfig, env: str, resume: bool) -> None:
    """
    CLI call for rebuilding a specific kubernetes environment
    Arguments:
        cfg (str): The rebuilder config.
        env (str): Environment to rebuild.
        fresh (bool): If the rebuilder should use the previous state file.
    """

    logging.info(f"Rebuilding environment {env}.")
    env_rebuild = Rebuild(env.lower(), env.lower(), cfg.access,
                          cfg.deployments, resume)

    env_rebuild.run_deployments()

    logging.info(f"Finished running deployments to {env}.")
