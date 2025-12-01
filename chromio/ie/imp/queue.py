from asyncio import Queue


class RecBatchQueue(Queue):
  """Queue with the record batches to import."""
