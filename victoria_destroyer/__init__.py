from victoria.plugin import Plugin
from .config import DestroyerSchema
from . import cli

# this object is loaded by Victoria and used as the plugin entry point
plugin = Plugin(name="destroyer",
                cli=cli.destroyer,
                config_schema=DestroyerSchema())
