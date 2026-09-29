from pydantic import BaseModel, Field
from typing import List

class Question(BaseModel):
    id: str = Field(..., description="Unique identifier for the question")
    category: str = Field(..., description="High‑level category, e.g., Python, DSA, HR")
    topic: str = Field(..., description="Specific topic within the category")
    difficulty: str = Field(..., description="beginner, intermediate, advanced")
    question: str = Field(..., description="Question text presented to the candidate")
    expected_concepts: List[str] = Field(..., description="Key concepts the answer should cover")
    ideal_answer_points: List[str] = Field(..., description="Bullet points of an ideal answer")
    recommended_material_topics: List[str] = Field(..., description="Topics for further study")
