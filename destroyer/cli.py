"""cli.py

This is the module that contains the Click CLI for the Destroyer

Author:
    Alex Potter-Dixon <apotter-dixon@glasswallsolutions.com>
"""

import click
import logging

from destroyer import config
from rebuild import Rebuild


@click.group()
def destroyer():
    """Wrapper for cli"""
    pass


@destroyer.command()
@click.argument('cfg', default="./config.yaml", type=click.Path(exists=True))
@click.option('--env',
              required=True,
              type=str,
              prompt="Environment",
              help="Environment you want to rebuild.")
def rebuild(cfg: str, env: str) -> None:
    """
    CLI call for rebuilding a specific kubernetes environment
    Arguments:
        cfg (str): Path to the config file.
        env (str): Environment to rebuild.  
    """
    destroyer_config = config.load(cfg)

    logging.info(f"Rebuilding environment {env} ")
    env_rebuild = Rebuild(
        env,
        destroyer_config.access,
        destroyer_config.deployments,
    )

    env_rebuild.run_deployments()

    logging.info(f"Successfully built {env}")


def main():
    """Main wrapper for CLI entry point"""
    destroyer()


if __name__ == '__main__':
    main()
