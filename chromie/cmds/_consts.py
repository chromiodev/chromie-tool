import typing

from chromadb.api.types import Space

# Embedding function names. [0] is the default value if needed.
EMBEDDING_FNS = ("default", "sentence_transformer")

# Space names.
SPACES = typing.get_args(Space)

# Default space.
DEFAULT_SPACE = "cosine"
