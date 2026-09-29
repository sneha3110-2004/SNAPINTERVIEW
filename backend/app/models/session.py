from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

from .question import Question

class InterviewConfig(BaseModel):
    role: str = Field(..., description="Interview role, e.g., Software Engineer")
    level: str = Field(..., description="Experience level, e.g., Entry")
    interview_type: str = Field(..., description="technical, hr, or mixed")
    duration: int = Field(..., description="Duration in minutes (5, 10, 15)")

class AnswerRecord(BaseModel):
    question_id: str = Field(..., description="ID of the question answered")
    answer_text: Optional[str] = Field(None, description="Candidate's answer text")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the answer was recorded")
    skipped: bool = Field(False, description="Whether the question was skipped")

class Session(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    config: InterviewConfig = Field(..., description="Interview configuration")
    status: Literal["pending", "in_progress", "completed"] = Field(..., description="Current status")
    current_question_index: int = Field(0, description="Index of the next question to present")
    question_ids: List[str] = Field(..., description="Ordered list of question IDs for this session")
    answers: List[AnswerRecord] = Field(default_factory=list, description="Answers recorded so far")
    started_at: datetime = Field(default_factory=datetime.utcnow, description="Start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp, if finished")
