from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Dict
from pydantic import BaseModel
from ..database import get_db
from ..models import Quiz, QuizAnswer, QuizAttempt, QuizStats

router = APIRouter(prefix="/api/stats", tags=["stats"])

class AnswerStats(BaseModel):
    answer: str
    correct_count: int
    attempt_count: int
    percentage: float

class QuizStatistics(BaseModel):
    quiz_id: int
    total_attempts: int
    average_score: float
    answers_stats: List[AnswerStats]

@router.get("/quizzes/{quiz_id}", response_model=QuizStatistics)
async def get_quiz_statistics(quiz_id: int, db: AsyncSession = Depends(get_db)):
    # Get quiz and verify it exists
    result = await db.execute(select(Quiz).filter(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get total attempts and average score
    attempts_result = await db.execute(
        select(
            func.count(QuizAttempt.id).label("total_attempts"),
            func.avg(QuizAttempt.score).label("average_score")
        ).filter(QuizAttempt.quiz_id == quiz_id)
    )
    attempts_stats = attempts_result.first()
    total_attempts = attempts_stats[0] or 0
    average_score = float(attempts_stats[1] or 0)
    
    # Get answer statistics
    answers_result = await db.execute(
        select(
            QuizAnswer.correct_answer,
            QuizStats.correct_count,
            QuizStats.attempt_count
        ).join(
            QuizStats,
            QuizAnswer.id == QuizStats.answer_id
        ).filter(
            QuizAnswer.quiz_id == quiz_id
        ).order_by(QuizAnswer.position)
    )
    answers = answers_result.all()
    
    answers_stats = []
    for answer in answers:
        correct_count = answer[1] or 0
        attempt_count = answer[2] or 0
        percentage = (correct_count / attempt_count * 100) if attempt_count > 0 else 0
        answers_stats.append(AnswerStats(
            answer=answer[0],
            correct_count=correct_count,
            attempt_count=attempt_count,
            percentage=percentage
        ))
    
    return QuizStatistics(
        quiz_id=quiz_id,
        total_attempts=total_attempts,
        average_score=average_score,
        answers_stats=answers_stats
    )
