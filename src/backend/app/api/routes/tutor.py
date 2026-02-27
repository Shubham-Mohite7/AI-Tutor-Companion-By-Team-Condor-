"""
tutor.py — FastAPI route handlers
"""

import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    TopicRequest,
    LearnResponse,
    ScoreRequest,
    ScoreResponse,
    AdaptiveQuestionRequest,
    AdaptiveQuestionResponse,
    TrueOrFalseRequest,
    TrueOrFalseResponse,
)
from app.services import ai_service
from app.services import true_false_service

logger = logging.getLogger(__name__)
router = APIRouter(tags=["tutor"])


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.options("/learn")
async def learn_options():
    return {"status": "ok"}

@router.post("/learn", response_model=LearnResponse)
async def learn(req: TopicRequest):
    try:
        return await ai_service.generate_learn_response(req.topic, req.language)
    except Exception as e:
        logger.exception(f"Error generating learn response for topic '{req.topic}'")
        error_msg = str(e) if str(e) else type(e).__name__
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/score", response_model=ScoreResponse)
async def score(req: ScoreRequest):
    results = []
    correct = 0
    for q, user_ans in zip(req.quiz, req.answers):
        is_correct = user_ans == q.correct_answer
        if is_correct:
            correct += 1
        results.append(
            {
                "question": q.question,
                "user_answer": user_ans,
                "correct_answer": q.correct_answer,
                "is_correct": is_correct,
                "explanation": q.explanation,
            }
        )
    total = len(req.quiz)
    return ScoreResponse(
        score=correct,
        total=total,
        percentage=round(correct / total * 100, 1) if total else 0,
        results=results,
    )


# ── Adaptive question ──────────────────────────────────────────────────────────

@router.post("/adaptive-question", response_model=AdaptiveQuestionResponse)
async def adaptive_question(req: AdaptiveQuestionRequest):
    """
    Generate the next MCQ adaptively:
    - Correct answer → harder question (difficulty + 2)
    - Wrong answer   → easier question (difficulty - 2)
    """
    try:
        return await ai_service.generate_adaptive_question(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── True/False Swipe Cards ─────────────────────────────────────────────────────

@router.post("/true-false", response_model=TrueOrFalseResponse)
async def true_false_cards(req: TrueOrFalseRequest):
    """
    Generate True/False statements from explanation for swipeable cards.
    Students swipe left (False) or right (True) to answer.
    """
    try:
        return await true_false_service.generate_true_false_statements(
            req.topic, req.explanation, req.language
        )
    except Exception as e:
        logger.exception(f"Error generating True/False statements for '{req.topic}'")
        raise HTTPException(status_code=500, detail=str(e))