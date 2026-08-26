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
