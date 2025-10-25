from dataclasses import dataclass
from pathlib import Path
from typing import Any, override

from aiofiles import ospath as path

from chromio.ie.ck import ExpFileChecker
from chromio.ie.dl.gh import GitHubDownloader
from chromio.tools import Cmd


@dataclass(frozen=True)
class DlCmd(Cmd):
  # @override
  name: str = "dl"

  # @override
  help: str = "Download a dataset stored in the Chromie hub."

  @property
  @override
  def args(self) -> list[dict]:
    return [
      {
        "names": ["path"],
        "help": "dataset dir path to download",
        "required": True,
      },
      {
        "names": ["dst"],
        "help": "path where to save the dataset",
        "default": Path("."),
        "type": Path,
      },
      {
        "names": ["--lang", "-l"],
        "help": "language to download",
        "choices": ("EN", "en", "ES", "es", "IT", "it"),
        "default": "EN",
      },
      {
        "names": ["--check", "-c"],
        "help": "Do validate the file downloaded w/ the Chromie Schema",
        "action": "store_true",
        "default": False,
      },
    ]

  @override
  async def _handle(self, args: Any) -> None:
    # (1) args
    stat, lang = args.path, args.lang.lower()
    if await path.isdir(dst := args.dst):
      dst = dst / (Path(stat).name + f"-{lang}.json")

    # (2) download
    print(f"Downloading '{stat}' to '{dst}'...")
    dl = GitHubDownloader()
    await dl.download(stat, dst, lang=lang)

    # (3) validate file if requested
    if args.check:
      print(f"Checking '{dst}'...")
      checker = ExpFileChecker()
      await checker.check(dst)
