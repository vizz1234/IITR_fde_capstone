"""
Tests for retrieve module: Acceptance Criterion A4.
Verifies vector store search against documentation corpus returns identifiable source passages with valid document IDs.
"""

from src.retrieve import get_retriever


def test_retrieval_returns_valid_doc_ids():
    retriever = get_retriever()
    results = retriever.search("How do I fix a container health check deployment failure?", top_k=3)
    assert len(results) > 0
    for passage in results:
        assert passage.doc_id.startswith("DOC-")
        assert passage.title != ""
        assert passage.score >= 0.0


def test_retrieval_irrelevant_query_threshold():
    retriever = get_retriever()
    # Query completely unrelated to cloud infrastructure
    results = retriever.search("qwertyuiop asdfghjkl zxcvbnm non_existent_gibberish_12345", top_k=3, score_threshold=0.85)
    # Thresholding should return empty or low score
    assert len(results) == 0 or all(r.score < 0.85 for r in results)
