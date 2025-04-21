from pydantic import BaseModel, Field


class PostQuestionStreamGeneratorType(BaseModel):
    id: str = Field(..., description="Unique identifier for the question")
    question: str = Field(..., description="The question to be asked")
    collection_name: str = Field(..., description="Where the document want to search")

    # Add validation
    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "question": "What is the meaning of life?",
                "collection_name": "test_collection"
            }
        }
