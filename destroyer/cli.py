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
from creator import create_environment


@click.group()
def destroyer():
    """Wrapper for cli"""
    pass


@destroyer.command()
def destroy() -> None:
    pass


@destroyer.command()
@click.argument('cfg', default="./config.yaml", type=click.Path(exists=True))
@click.argument('env', default='pent', type=str)
def rebuild(cfg: str, env: str) -> None:
    destroyer_config = config.load(cfg)
    create_environment(
        destroyer_config.environments,
        destroyer_config.access,
        destroyer_config.deployments,
    )
    print(destroyer_config.environments)

    pass


def main():
    destroyer()


if __name__ == '__main__':
    main()