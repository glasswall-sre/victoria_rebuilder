"""cli.py

This is the module that contains the Click CLI for the Destroyer

Author:
    Alex Potter-Dixon <apotter-dixon@glasswallsolutions.com>
"""
import logging
from typing import List, Iterable

import click
import sys



@click.group()
def destroyer():
    """Wrapper for cli"""
    pass
  

@destroyer.command()
def destroy() -> None:
    pass
def main():
    destroyer()

if __name__ == '__main__':
    main()