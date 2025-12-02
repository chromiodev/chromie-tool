from abc import ABC
from dataclasses import dataclass

from ._queue import RecBatchQueue


@dataclass
class RecBatchWriter(ABC):
  """A worker for inserting record batches in somewhere from an asynchronous queue."""

  queue: RecBatchQueue
  """Queue with the record batches to import."""
