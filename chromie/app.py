import asyncio
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from importlib.metadata import version
from typing import Self, final

from dotenv import load_dotenv

from .cmds.check import CheckCmd
from .cmds.cp import CpCmd
from .cmds.dl import DlCmd
from .cmds.exp import ExpCmd
from .cmds.imp import ImpCmd
from .cmds.ls import LsCmd
from .cmds.ping import PingCmd
from .cmds.uri import UriCmd

# CLI commands.
Cmds = (UriCmd, PingCmd, LsCmd, CpCmd, CheckCmd, ExpCmd, DlCmd, ImpCmd)


@final
class ChromieArgParser(ArgumentParser):
  """The argument parser for the chromie app."""

  def __init__(self, **kwargs):
    # this can be called from us but from add_subparsers() too;
    # in this last case, kwargs are passed. We don't pass/use kwargs
    if len(kwargs) > 0:
      super().__init__(**kwargs)
    else:
      super().__init__(
        prog="chromie",
        description="Chroma import/export.",
        formatter_class=ArgumentDefaultsHelpFormatter,
      )

      self._define_commands()

  def _define_commands(self) -> Self:
    """Defines the commands of the CLI.

    Observations:
      When the user passes nothing, the help must be shown.
    """

    # (1) create parser
    self.add_argument(
      "--version", action="version", version=f"v{version('chromie-tool')}"
    )
    self.set_defaults(func=lambda _: self.print_help())

    # (2) define commands
    sp = self.add_subparsers(title="commands")

    for Cmd in Cmds:
      cmd = Cmd()
      cmd.define(sp)

    # (3) return
    return self

  async def parse_args_and_run(self, argv: list[str]) -> None:
    """Parses the arguments and run this requested by the user.

    Args:
      args: Arguments passed by the user in the command line.
    """

    args = self.parse_args(argv)

    if (co := args.func(args)) is not None:
      await co


async def main() -> None:
  # (1) pre
  load_dotenv()

  # (2) run
  code = 0  # exit code

  try:
    parser = ChromieArgParser()
    await parser.parse_args_and_run(sys.argv[1:])
  except Exception as e:
    print(e, file=sys.stderr)
    code = 1

  exit(code)


def run() -> None:
  asyncio.run(main())
