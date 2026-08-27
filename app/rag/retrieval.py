from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.document import DocumentChunk
from app.rag.embeddings import get_embedding


def retrieve_relevant_chunks(db: Session, query: str, top_k: int = 3):
    query_embedding = get_embedding(query)

    results = (
        db.query(DocumentChunk)
        .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
        .limit(top_k)
        .all()
    )

    return results
