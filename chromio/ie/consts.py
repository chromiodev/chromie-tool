from .field import Field

DEFAULT_BATCH_SIZE = 250
"""Default size for the R/W batches."""

DEFAULT_FIELDS: list[Field] = [Field.id, Field.meta, Field.doc]
"""Default fields to import/export."""

DEFAULT_WRITERS = 2
"""Default number of writer workers to use in the imports."""

DEFAULT_READERS = 2
"""Default number of reader workers to use in the exports."""
