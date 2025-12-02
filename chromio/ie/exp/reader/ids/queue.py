from asyncio import Queue


class IdBatchQueue(Queue):
  """Queue with the identifier batches to read."""
