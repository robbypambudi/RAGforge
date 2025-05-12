from pydantic import BaseModel

from app.utils.schema import as_form


@as_form
class BaseQuestion(BaseModel):
    question_id: str
    question_text: str


class QuestionResponse(BaseModel):
    question_id: str
    question_text: str
    answer: str
