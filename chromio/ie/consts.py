from .field import Field

DEFAULT_BATCH_SIZE = 200
"""Default size for the R/W batches."""

DEFAULT_FIELDS: list[Field] = [Field.id, Field.meta, Field.doc]
"""Default fields to import/export."""
