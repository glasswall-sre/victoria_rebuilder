"""cli.py

This is the module that contains the Click CLI for V.I.C.T.O.R.I.A rebuilder

Author:
    Alex Potter-Dixon <apotter-dixon@glasswallsolutions.com>
"""

import logging

import click

from .config import RebuilderConfig, AccessConfig
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
        cfg (RebuilderConfig): The rebuilder config.
        from_env (str): The environment to rebuild from in Azure DevOps.
        to_env (str): The environment to rebuild.
        resume (bool): If the rebuilder should resume using previous state file.

    """
    logging.info(
        f"Rebuilding environments {from_env} from environment: {to_env}")

    logging.info(f"Rebuilding environment {to_env}.")

    access_cfg = retrieve_access_config(cfg)
    env_rebuild = Rebuild(from_env.lower(), to_env.lower(), access_cfg,
                          cfg.deployments, resume)

    env_rebuild.run_deployments()

    logging.info(f"Finished running deployments to {to_env}.")


@rebuilder.command()
@click.argument('env', nargs=1, type=str)
@click.option(
    '-r',
    '--resume',
    is_flag=True,
    help="If you want the rebuilder to use the previous state file.")
@click.option(
    '-a',
    '--auto-retry',
    is_flag=True,
    help="If a release fails to deploy, instead of prompting the user for a y/n on retry, it automatically retries "
         "the deployment.")
@click.pass_obj
def rebuild(cfg: RebuilderConfig, env: str, resume: bool, auto_retry: bool) -> None:
    """
    CLI call for rebuilding a specific kubernetes environment
    Arguments:
        cfg (RebuilderConfig): The rebuilder config.
        env (str): Environment to rebuild.
        resume (bool): If the rebuilder should use the previous state file.
        auto_retry (bool): If a release fails to deploy, instead of prompting the user for a y/n on retry, it automatically retries the deployment.
    """
    logging.info(f"Rebuilding environment {env}.")

    access_cfg = retrieve_access_config(cfg)
    env_rebuild = Rebuild(env.lower(), env.lower(), access_cfg,
                          cfg.deployments, resume, auto_retry)

    env_rebuild.run_deployments()

    logging.info(f"Finished running deployments to {env}.")


def retrieve_access_config(cfg: RebuilderConfig) -> AccessConfig:
    try:
        encryption_provider = cfg.victoria_config.get_encryption()
    except AttributeError:
        logging.error(
            "Please specify 'provider' in the Victoria settings.")
        raise SystemExit(1)
    else:
        access_token = encryption_provider.decrypt_str(cfg.access.access_token)
        email = encryption_provider.decrypt_str(cfg.access.email)
        organisation = encryption_provider.decrypt_str(cfg.access.organisation)
        project = encryption_provider.decrypt_str(cfg.access.project)

        if None in [access_token, email, organisation, project]:
            logging.error(
                "Invalid 'access' settings provided. Unable to decrypt.")
            raise SystemExit(1)

        return AccessConfig(access_token=access_token, email=email, organisation=organisation, project=project)
