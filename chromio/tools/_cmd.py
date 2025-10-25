from abc import ABC, abstractmethod
from argparse import ArgumentDefaultsHelpFormatter, _SubParsersAction
from dataclasses import dataclass
from typing import Any, final


@dataclass(frozen=True)
class Cmd(ABC):
  """A command associated to a Chromio tool."""

  name: str
  """Command name such as, for example, export."""

  help: str
  """Command help."""

  @final
  def define(self, sp: _SubParsersAction) -> None:
    """Defines the command in the given parser.

    Args:
      sp: Argument parser where to define it.
    """

    # (1) create its command parer
    (
      cmd := sp.add_parser(
        self.name,
        help=self.help,
        formatter_class=ArgumentDefaultsHelpFormatter,
      )
    ).set_defaults(func=self.handle)

    # (2) define arguments
    for arg in self.args:
      # common extra options
      extra_opts = {}

      for opt in ("default", "metavar", "type", "nargs"):
        if opt in arg:
          extra_opts[opt] = arg[opt]

      # define argument
      if arg["names"][0].startswith("-"):  # named
        cmd.add_argument(
          *arg["names"],
          action=arg.get("action", "store"),
          help=arg["help"],
          required=arg.get("required", False),
          **extra_opts,
        )
      else:  # positional
        if not arg.get("required", False):
          extra_opts["nargs"] = "?"

        cmd.add_argument(
          *arg["names"],
          action=arg.get("action", "store"),
          help=arg["help"],
          **extra_opts,
        )

  @property
  @abstractmethod
  def args(self) -> list[dict]:
    """The arguments associated to the command."""

  @final
  async def handle(self, args: Any) -> None:
    """Handles the command.

    Args:
      args: The arguments passed to the command.
    """

    await self._handle(args)

  @abstractmethod
  async def _handle(self, args: Any) -> None:
    """Handles the command.

    Args:
      args: The arguments passed to the command.
    """
