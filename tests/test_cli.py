import click
from click.testing import CliRunner
from victoria_rebuilder import cli

def test_rebuild_extra_argument_fail():
   

    runner = CliRunner()
    result = runner.invoke(cli.rebuild, ['qa', 'pent'])
    assert result.exit_code == 2



def test_rebuild():
   

    runner = CliRunner()
    result = runner.invoke(cli.rebuild, ['qa'])
    print(result)
    assert result.exit_code == 1

