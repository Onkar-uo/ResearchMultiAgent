from app.rag.ingestion import ingest_document
from app.rag.vector_store import SQLiteVectorStore


class FakeEmbeddings:
    def embed_documents(self, texts):
        return [[1.0, 0.0] for _ in texts]


def test_ingestion_removes_stale_chunks_when_document_shrinks(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()
    document = knowledge_dir / "guide.md"
    document.write_text("stale content " * 250, encoding="utf-8")
    store = SQLiteVectorStore(tmp_path / "vectors.sqlite3")

    first_count = ingest_document(
        document,
        store=store,
        embeddings=FakeEmbeddings(),
        knowledge_dir=knowledge_dir,
    )
    document.write_text("current content", encoding="utf-8")
    second_count = ingest_document(
        document,
        store=store,
        embeddings=FakeEmbeddings(),
        knowledge_dir=knowledge_dir,
    )

    assert first_count > 1
    assert second_count == 1
    indexed = store.document("guide.md")
    assert len(indexed) == 1
    assert indexed[0]["content"] == "current content"
