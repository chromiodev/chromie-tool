from dataclasses import dataclass
from typing import Any, override

import pytest
from pytest_mock import MockerFixture

from chromio.tools import Cmd


@pytest.fixture(scope="module")
def TestCmd() -> type:
  """Command class to use in the tests."""

  @dataclass(frozen=True)
  class TestCmd(Cmd):
    name: str = "test"
    help: str = "Test command help."

    @property
    @override
    def args(self) -> list[dict]:
      return [
        {"names": ["--opt1"], "help": "opt1 help", "metavar": "opt1"},
        {"names": ["--opt2"], "help": "opt2 help"},
        {"names": ["arg1"], "help": "arg1 help"},
      ]

    @override
    async def _handle(self, args: Any) -> None:
      raise ValueError("called!")

  return TestCmd


def test_define(mocker: MockerFixture, TestCmd: type) -> None:
  """Check that define() defines the arguments as expected."""

  # (1) arrange
  action = mocker.Mock()
  (add_parser := action.add_parser).return_value = (cmd := mocker.Mock())
  (set_defaults := cmd.set_defaults).return_value = None
  (add_argument := cmd.add_argument).return_value = None

  # (2) act
  TestCmd().define(action)

  # (3) assessment
  assert add_parser.call_count == 1
  assert set_defaults.call_count == 1
  assert add_argument.call_count == 3


async def test_handle(mocker: MockerFixture, TestCmd: type) -> None:
  """Check that handle() calls to _handle()."""

  # (1) arrange
  action = mocker.Mock()
  action.add_parser.return_value = mocker.Mock()

  # (2) act and assessment
  with pytest.raises(ValueError, match="called!"):
    (cmd := TestCmd()).define(action)
    await cmd.handle(type("Args", (object,), {}))
