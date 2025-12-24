# Placeholder tests for the future indexer chunker implementation.
# These ensure the basic contract: header-aware chunking within size bounds.

import textwrap


def test_chunker_basic_contract() -> None:
    from services.indexer.chunker import chunk_text  # type: ignore

    text = "\n".join([f"Heading {i}\n" + "Lorem ipsum " * 80 for i in range(3)])

    chunks = list(chunk_text(text))

    assert chunks, "chunk_text should return at least one chunk"
    for chunk in chunks:
        assert 200 <= len(chunk.text) <= 4000
      
