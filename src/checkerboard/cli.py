"""Administrative command-line interface."""

__all__ = ["main", "help", "run"]

from typing import Union

import click
from aiohttp.web import run_app

from checkerboard.app import create_app


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(message="%(version)s")
def main() -> None:
    """checkerboard

    Administrative command-line interface for checkerboard.
    """
    pass


@main.command()
@click.argument("topic", default=None, required=False, nargs=1)
@click.pass_context
def help(ctx: click.Context, topic: Union[None, str]) -> None:
    """Show help for any command."""
    # The help command implementation is taken from
    # https://www.burgundywall.com/post/having-click-help-subcommand
    if topic:
        if topic in main.commands:
            click.echo(main.commands[topic].get_help(ctx))
        else:
            raise click.UsageError(f"Unknown help topic {topic}", ctx)
    else:
        assert ctx.parent
        click.echo(ctx.parent.get_help())


@main.command()
@click.option(
    "--port", default=8080, type=int, help="Port to run the application on."
)
def run(port: int) -> None:
    """Run the application (for production)."""
    app = create_app()
    run_app(app, port=port)
