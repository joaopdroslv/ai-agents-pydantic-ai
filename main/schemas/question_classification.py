from pydantic import BaseModel, Field


class QuestionClassification(BaseModel):
    text: str
    difficult_level: int = Field(
        ge=0, ke=10, description="Question difficulty level, from 0 to 10."
    )
