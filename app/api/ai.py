from fastapi import APIRouter, Depends
from app.ml.predict import predict_ticket_labels
from app.schemas.ai import ClassifyRequest, ClassifyResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])


@router.post("/classify", response_model=ClassifyResponse)
def classify_ticket_text(
    request: ClassifyRequest,
    current_user: User = Depends(get_current_user),
):
    result = predict_ticket_labels(request.text)
    return result


from sqlalchemy.orm import Session
from database import get_db
from app.rag.retrieval import retrieve_relevant_chunks
from app.rag.generation import generate_answer
from app.schemas.ai import ChatRequest, ChatResponse, SourceChunk


@router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chunks = retrieve_relevant_chunks(db, request.question, top_k=3)

    if not chunks:
        return ChatResponse(
            answer="I couldn't find this information in the available campus documents.",
            sources=[],
        )

    context_texts = [chunk.content for chunk in chunks]
    answer = generate_answer(request.question, context_texts)

    sources = [
        SourceChunk(
            document_filename=chunk.document.filename,
            chunk_index=chunk.chunk_index,
            content_preview=chunk.content[:150],
        )
        for chunk in chunks
    ]

    return ChatResponse(answer=answer, sources=sources)
