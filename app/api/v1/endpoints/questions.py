from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.middleware import inject
from app.schema.base_schema import BaseResponse
from app.schema.question_schema import QuestionResponse, BaseQuestion
from app.services.question_service import QuestionService

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("", tags=["get"], response_model=BaseResponse[QuestionResponse])
@inject
def question_with_stream(
        payload: BaseQuestion = Depends(),
        question_service: QuestionService = Provide[Depends(Container.question_service)]
):
    """
    Get a list of questions
    """
    return BaseResponse(
        message="Questions retrieved successfully",
        data=QuestionResponse(
            question_id=payload.question_id,
            question_text="What is the capital of France?",
            answer="The capital of France is Paris."
        )
    )
