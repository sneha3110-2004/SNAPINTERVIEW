from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uuid
from datetime import datetime

from ..models.question import Question
from ..data.question_bank import QUESTION_BANK

router = APIRouter()
from ..models.session import Session, InterviewConfig, AnswerRecord

# In-memory session store
SESSION_STORE: Dict[str, Session] = {}

# Duration to question count mapping
DURATION_MAP = {
    5: 4,
    10: 8,
    15: 12,
}

class CreateSessionRequest(BaseModel):
    duration_minutes: int = Field(..., description="Interview duration in minutes (5, 10, or 15)")
    interview_type: str = Field(..., description="Type of interview, e.g., 'technical' or 'mixed'")

class CreateSessionResponse(BaseModel):
    session_id: str
    questions: List[Question]
    start_timestamp: str



class SessionStatusResponse(BaseModel):
    session_id: str
    current_index: int
    total_questions: int
    started_at: str
    completed_at: Optional[str] = None

class ResultItem(BaseModel):
    question_id: str
    answer: Optional[str] = None
    skipped: bool
    answered_at: Optional[str] = None

class SessionResultsResponse(BaseModel):
    session_id: str
    results: List[ResultItem]
    started_at: str
    completed_at: Optional[str] = None

def _select_questions(interview_type: str, count: int) -> List[Question]:
    interview_type = interview_type.lower()
    if interview_type == "technical":
        filtered = [q for q in QUESTION_BANK if q.category.lower() != "hr"]
    elif interview_type == "hr":
        filtered = [q for q in QUESTION_BANK if q.category.lower() == "hr"]
    else:  # mixed
        filtered = list(QUESTION_BANK)
    filtered.sort(key=lambda q: q.id)
    return filtered[:count]

# @router.post("/session", response_model=CreateSessionResponse)
def create_session(req: CreateSessionRequest):
    if req.duration_minutes not in DURATION_MAP:
        raise HTTPException(status_code=400, detail="Invalid duration. Choose 5, 10, or 15 minutes.")
    num_q = DURATION_MAP[req.duration_minutes]
    questions = _select_questions(req.interview_type, num_q)
    if len(questions) < num_q:
        raise HTTPException(status_code=500, detail="Not enough questions in the bank.")
    session_id = str(uuid.uuid4())
    now_iso = datetime.utcnow().isoformat() + "Z"
    SESSIONS[session_id] = {
        "started_at": now_iso,
        "completed_at": None,
        "questions": questions,
        "answers": {},  # question_id -> dict
        "current_index": 0,
    }
    return CreateSessionResponse(session_id=session_id, questions=questions, start_timestamp=now_iso)

# @router.post("/session/{session_id}/answer", response_model=AnswerResponse)
def submit_answer(session_id: str, payload: AnswerSubmission):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session["current_index"] >= len(session["questions"]):
        raise HTTPException(status_code=400, detail="All questions already answered")
    current_q = session["questions"][session["current_index"]]
    if payload.question_id != current_q.id:
        raise HTTPException(status_code=400, detail="Question ID does not match current question")
    answered_at = datetime.utcnow().isoformat() + "Z"
    session["answers"][payload.question_id] = {
        "answer": payload.answer,
        "skipped": payload.skip,
        "answered_at": answered_at,
    }
    session["current_index"] += 1
    if session["current_index"] == len(session["questions"]):
        session["completed_at"] = answered_at
    return AnswerResponse(message="Answer recorded")

# @router.get("/session/{session_id}/status", response_model=SessionStatusResponse)
def get_status(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionStatusResponse(
        session_id=session_id,
        current_index=session["current_index"],
        total_questions=len(session["questions"]),
        started_at=session["started_at"],
        completed_at=session["completed_at"],
    )

# @router.get("/session/{session_id}/results", response_model=SessionResultsResponse)
def get_results(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    results = []
    for q in session["questions"]:
        ans = session["answers"].get(q.id)
        results.append(ResultItem(
            question_id=q.id,
            answer=ans["answer"] if ans else None,
            skipped=ans["skipped"] if ans else False,
            answered_at=ans["answered_at"] if ans else None,
        ))
    return SessionResultsResponse(
        session_id=session_id,
        results=results,
        started_at=session["started_at"],
        completed_at=session["completed_at"],
    )

# New interview endpoints

class StartInterviewRequest(BaseModel):
    role: str = Field(..., description="Interview role")
    level: str = Field(..., description="Experience level")
    interview_type: str = Field(..., description="technical, hr, or mixed")
    duration: int = Field(..., description="Duration in minutes (5, 10, 15)")

class StartInterviewResponse(BaseModel):
    session_id: str
    first_question: Question
    start_timestamp: str

class CurrentQuestionResponse(BaseModel):
    question: Question
    current_index: int
    total_questions: int

class AnswerRequest(BaseModel):
    answer: str

class AnswerResponse(BaseModel):
    message: str
    next_question: Optional[Question] = None
    completed: bool = False

class SkipResponse(BaseModel):
    message: str
    next_question: Optional[Question] = None
    completed: bool = False

class SummaryResponse(BaseModel):
    role: str
    level: str
    interview_type: str
    duration: int
    total_questions: int
    attempted: int
    skipped: int
    completed: bool

@router.post("/interview/start", response_model=StartInterviewResponse)
def start_interview(req: StartInterviewRequest):
    if req.duration not in DURATION_MAP:
        raise HTTPException(status_code=400, detail="Invalid duration")
    count = DURATION_MAP[req.duration]
    questions = _select_questions(req.interview_type, count)
    if len(questions) < count:
        raise HTTPException(status_code=500, detail="Not enough questions")
    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    session = Session(
        session_id=session_id,
        config=InterviewConfig(
            role=req.role,
            level=req.level,
            interview_type=req.interview_type,
            duration=req.duration,
        ),
        status="in_progress",
        current_question_index=0,
        question_ids=[q.id for q in questions],
        answers=[],
        started_at=now,
        completed_at=None,
    )
    SESSION_STORE[session_id] = session
    return StartInterviewResponse(
        session_id=session_id,
        first_question=questions[0],
        start_timestamp=now.isoformat() + "Z",
    )

@router.get("/interview/{session_id}", response_model=Session)
def get_session(session_id: str):
    session = SESSION_STORE.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/interview/{session_id}/current-question", response_model=CurrentQuestionResponse)
def get_current_question(session_id: str):
    session = SESSION_STORE.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status == "completed":
        raise HTTPException(status_code=400, detail="Interview already completed")
    idx = session.current_question_index
    total = len(session.question_ids)
    qid = session.question_ids[idx]
    question = next((q for q in QUESTION_BANK if q.id == qid), None)
    if not question:
        raise HTTPException(status_code=500, detail="Question not found")
    return CurrentQuestionResponse(
        question=question,
        current_index=idx + 1,
        total_questions=total,
    )

@router.post("/interview/{session_id}/answer", response_model=AnswerResponse)
def submit_answer(session_id: str, payload: AnswerRequest):
    session = SESSION_STORE.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status == "completed":
        raise HTTPException(status_code=400, detail="Interview already completed")
    idx = session.current_question_index
    if idx >= len(session.question_ids):
        raise HTTPException(status_code=400, detail="All questions already answered")
    qid = session.question_ids[idx]
    record = AnswerRecord(
        question_id=qid,
        answer_text=payload.answer,
        timestamp=datetime.utcnow(),
        skipped=False,
    )
    session.answers.append(record)
    session.current_question_index += 1
    completed = session.current_question_index >= len(session.question_ids)
    if completed:
        session.status = "completed"
        session.completed_at = datetime.utcnow()
        return AnswerResponse(message="Answer recorded", completed=True)
    next_qid = session.question_ids[session.current_question_index]
    next_question = next((q for q in QUESTION_BANK if q.id == next_qid), None)
    return AnswerResponse(message="Answer recorded", next_question=next_question, completed=False)

@router.post("/interview/{session_id}/skip", response_model=SkipResponse)
def skip_question(session_id: str):
    session = SESSION_STORE.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status == "completed":
        raise HTTPException(status_code=400, detail="Interview already completed")
    idx = session.current_question_index
    if idx >= len(session.question_ids):
        raise HTTPException(status_code=400, detail="All questions already answered")
    qid = session.question_ids[idx]
    record = AnswerRecord(
        question_id=qid,
        answer_text=None,
        timestamp=datetime.utcnow(),
        skipped=True,
    )
    session.answers.append(record)
    session.current_question_index += 1
    completed = session.current_question_index >= len(session.question_ids)
    if completed:
        session.status = "completed"
        session.completed_at = datetime.utcnow()
        return SkipResponse(message="Question skipped", completed=True)
    next_qid = session.question_ids[session.current_question_index]
    next_question = next((q for q in QUESTION_BANK if q.id == next_qid), None)
    return SkipResponse(message="Question skipped", next_question=next_question, completed=False)

@router.post("/interview/{session_id}/complete", response_model=SummaryResponse)
def complete_interview(session_id: str):
    session = SESSION_STORE.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status != "completed":
        session.status = "completed"
        session.completed_at = datetime.utcnow()
    attempted = len(session.answers)
    skipped = sum(1 for a in session.answers if a.skipped)
    return SummaryResponse(
        role=session.config.role,
        level=session.config.level,
        interview_type=session.config.interview_type,
        duration=session.config.duration,
        total_questions=len(session.question_ids),
        attempted=attempted,
        skipped=skipped,
        completed=session.status == "completed",
    )

@router.get("/interview/{session_id}/summary", response_model=SummaryResponse)
def get_summary(session_id: str):
    session = SESSION_STORE.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    attempted = len(session.answers)
    skipped = sum(1 for a in session.answers if a.skipped)
    return SummaryResponse(
        role=session.config.role,
        level=session.config.level,
        interview_type=session.config.interview_type,
        duration=session.config.duration,
        total_questions=len(session.question_ids),
        attempted=attempted,
        skipped=skipped,
        completed=session.status == "completed",
    )
