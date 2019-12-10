"""cli.py

This is the module that contains the Click CLI for the Destroyer

Author:
    Alex Potter-Dixon <apotter-dixon@glasswallsolutions.com>
"""
import logging
from typing import List, Iterable

import click
import sys
import config
from rebuild import rebuild_environment


@click.group()
def destroyer():
    """Wrapper for cli"""
    pass


@destroyer.command()
def destroy() -> None:
    pass


@destroyer.command()
@click.argument('cfg', default="./config.yaml", type=click.Path(exists=True))
@click.argument('env', default='dev', type=str)
def rebuild(cfg: str, env: str) -> None:
    destroyer_config = config.load(cfg)
    rebuild_environment(
        env,
        destroyer_config.access,
        destroyer_config.deployments,
    )


def main():
    destroyer()


if __name__ == '__main__':
    main()