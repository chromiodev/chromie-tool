#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path
from typing import Any

from llama_index.core.llms import LLM
from llama_index.llms.google_genai import GoogleGenAI

# Directory path where this module is.
mod_dir = Path(__file__).parent

# Docs directory path.
docs_dir = mod_dir / ".." / "docs"

# Gemini directory path.
gemini_dir = mod_dir / ".." / ".gemini"

# Default model to use.
default_model = "gemini-2.5-pro"

# System prompt to use in the LLM model.
sys_prompt = """
Translate the documentation for a Python project related to vector databases, concretely Chroma.
The documentation is written in Markdown and the result must be too.
Observations that you must keep in mind:

- When translating, keep the original format, including titles, lists, code blocks, etc.

- If the source Markdown contains links to another documents with the .es.md extension,
  in the destination these must be .en.md.

- You mustn't capitalize the use cases in the titles.

- When needed, you use pre-conditions and post-conditions instead of preconditions and
  postconditions, respectively.
"""


def _translate_file(file: Path, llm: LLM) -> str:
  """Translate a given file.

  Args:
    file: Source file path to translate.
    llm: LLM to use for the translation.

  Returns:
    Translated content.
  """

  # (1) read the content
  c = file.read_text()

  # (2) translate
  prompt = f"""
  Content language to translate: ES (Spain).
  Destination language: EN (US).
  Content to translate:
  {c}
  """

  resp = llm.complete(
    prompt=sys_prompt + "\n\n" + prompt,
    stream=False,
  )

  # (3) return
  return resp.text


def _translate_dir(
  dir: Path, src_ext: str, dst_ext: str, model: str, force: bool
) -> None:
  """Translate the files of a specific directory.

  Args:
    dir: Directory path to translate.
    src_ext: Extension for the files to translate such as, for example, .es.md or .md.
    dst_ext: Extension for the translated files.
    model: Model to use for the translation.
    force: Force the translation even if the destination file is newer than the source.
  """

  # (1) prepare context
  llm = GoogleGenAI(model=model, temperature=0.1)

  # (2) translate files
  for src in dir.rglob(rf"*{src_ext}", recurse_symlinks=True):
    dst = src.parent / src.name.replace(src_ext, dst_ext)

    # translate
    if force or not dst.exists() or (src.stat().st_mtime > dst.stat().st_mtime):
      print(f"Translating {src} to {dst}...", flush=True)
      dst.write_text(_translate_file(src, llm))


def handle_translate(args: Any) -> None:
  """Translate a specific content directory."""

  # (1) precondition
  if os.getenv("GOOGLE_API_KEY") is None:
    print("ERROR: GOOGLE_API_KEY environment variable unset.", file=sys.stderr)
    exit(1)

  # (2) args
  force = args.force

  # (3) translate
  for dir in (arg,) if (arg := args.dir) != "all" else ("docs", "gemini"):
    match dir:
      case "docs":
        _translate_dir(docs_dir, ".es.md", ".en.md", default_model, force)

      case "gemini":
        _translate_dir(gemini_dir, ".es.md", ".md", default_model, force)


########
# main #
########

# (1) define script
parser = ArgumentParser(
  prog="doc",
  description="Tool for translating README.md files.",
  formatter_class=ArgumentDefaultsHelpFormatter,
)

sp = parser.add_subparsers(title="commands")

# translate
(
  cmd := sp.add_parser(
    "trans",
    help="Translate a content directory.",
    formatter_class=ArgumentDefaultsHelpFormatter,
  )
).set_defaults(func=handle_translate)

cmd.add_argument(
  "dir",
  help="Directory to translate",
  action="store",
  choices=("all", "docs", "gemini"),
)

cmd.add_argument(
  "--force",
  "-f",
  help="Force translation even if the destination file is newer than the source.",
  action="store_true",
  default=False,
)

# (2) run script
args = parser.parse_args()
args.func(args)
