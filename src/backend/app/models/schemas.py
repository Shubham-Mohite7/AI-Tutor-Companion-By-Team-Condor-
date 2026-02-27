from pydantic import BaseModel
from typing import Optional


class TopicRequest(BaseModel):
    topic: str
    language: str = "en"


class QuizQuestion(BaseModel):
    question: str
    options: list[str]          # ["A) ...", "B) ...", "C) ...", "D) ..."]
    correct_answer: str
    explanation: str
    difficulty: int = 5         # 1-10 scale (1=easiest, 10=hardest)


class LearnResponse(BaseModel):
    topic: str
    explanation: str
    quiz: list[QuizQuestion]


class ScoreRequest(BaseModel):
    quiz: list[QuizQuestion]
    answers: list[Optional[str]]


class ScoreResponse(BaseModel):
    score: int
    total: int
    percentage: float
    results: list[dict]


# ── Adaptive Quiz ──────────────────────────────────────────────────────────────

class AdaptiveQuestionRequest(BaseModel):
    topic: str
    explanation: str            # original explanation for context
    last_question: QuizQuestion
    was_correct: bool
    language: str = "en"


class AdaptiveQuestionResponse(BaseModel):
    question: QuizQuestion
    difficulty_change: str      # "harder" | "easier" | "same"
    new_difficulty: int


# ── True/False Swipe Cards ──────────────────────────────────────────────────────

class TrueOrFalseStatement(BaseModel):
    id: int
    statement: str              # The statement to evaluate
    is_true: bool               # Correct answer: True or False
    explanation: str            # Why it's true or false


class TrueOrFalseRequest(BaseModel):
    topic: str
    explanation: str
    language: str = "en"


class TrueOrFalseResponse(BaseModel):
    topic: str
    statements: list[TrueOrFalseStatement]