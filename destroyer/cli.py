"""cli.py

This is the module that contains the Click CLI for the Destroyer

Author:
    Alex Potter-Dixon <apotter-dixon@glasswallsolutions.com>
"""

import click

from destroyer import config
from rebuild import Rebuild


@click.group()
def destroyer():
    """Wrapper for cli"""
    pass


@destroyer.command()
def destroy() -> None:
    """Destroyer placeholder"""
    pass


@destroyer.command()
@click.argument('cfg', default="./config.yaml", type=click.Path(exists=True))
@click.argument('env', default='dev', type=str)
def rebuild(cfg: str, env: str) -> None:
    """CLI call for rebuilding a specific kubernetes environment"""
    destroyer_config = config.load(cfg)
    env_rebuild = Rebuild(
        env,
        destroyer_config.access,
        destroyer_config.deployments,
    )

    env_rebuild.run_deployments()


def main():
    """Main wrapper for CLI entry point"""
    destroyer()


if __name__ == '__main__':
    main()
