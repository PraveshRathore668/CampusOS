import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.models.document import Document, DocumentChunk
from app.models.user import User, RoleEnum
from app.schemas.document import DocumentUploadResponse
from app.api.deps import get_current_user, require_role
from app.rag.chunking import extract_text_from_pdf, extract_text_from_txt, clean_text, chunk_text
from app.rag.embeddings import get_embedding

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])

UPLOAD_DIR = "uploaded_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN, RoleEnum.FACULTY)),
):
    filename = file.filename
    extension = filename.split(".")[-1].lower()

    if extension not in ("pdf", "txt"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and TXT files are supported",
        )

    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if extension == "pdf":
        raw_text = extract_text_from_pdf(file_path)
    else:
        raw_text = extract_text_from_txt(file_path)

    cleaned = clean_text(raw_text)
    chunks = chunk_text(cleaned)

    new_document = Document(
        filename=filename,
        document_type=extension.upper(),
        uploaded_by=current_user.id,
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    for index, chunk_content in enumerate(chunks):
        embedding = get_embedding(chunk_content)
        chunk = DocumentChunk(
            document_id=new_document.id,
            chunk_index=index,
            content=chunk_content,
            embedding=embedding,
        )
        db.add(chunk)

    db.commit()

    return DocumentUploadResponse(document=new_document, chunks_created=len(chunks))
