from victoria.plugin import Plugin
from .config import RebuilderSchema
from . import cli

# this object is loaded by Victoria and used as the plugin entry point
plugin = Plugin(name="rebuilder",
                cli=cli.rebuilder,
                config_schema=RebuilderSchema())
