from abc import ABC
from dataclasses import dataclass

from ._queue import RecBatchQueue


@dataclass
class RecBatchReader(ABC):
  """A worker for reading Chroma records and producing its batches
  to an asynchronous queue.
  """

  queue: RecBatchQueue
  """Asynchronous queue where to insert the record batches."""
