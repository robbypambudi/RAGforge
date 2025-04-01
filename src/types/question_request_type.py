from pydantic import BaseModel, Field

class PostQuestionStreamGeneratorType(BaseModel):
  id: str = Field(..., description="Unique identifier for the question")
  question: str = Field(..., description="The question to be asked")