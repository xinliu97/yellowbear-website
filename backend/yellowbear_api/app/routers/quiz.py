from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Optional, Union
from pydantic import BaseModel, validator
from ..database import get_db
from ..models import Quiz, QuizAnswer, QuizAttempt, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])

class AnswerCreate(BaseModel):
    correct_answer: str
    aliases: List[str] = []
    position: int
    is_correct: bool = False  # For multiple choice: whether this option is correct
    explanation: Optional[str] = None  # Optional explanation for why this answer is correct/incorrect

class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None
    quiz_type: str  # "list" or "multiple_choice"
    time_limit: Optional[int] = None
    answers: Optional[List[AnswerCreate]] = []
    is_multiple_choice: bool = False
    allow_multiple_answers: bool = False

class QuizResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    quiz_type: str
    time_limit: Optional[int]
    attempt_count: int
    creator_id: int

    class Config:
        from_attributes = True

class AttemptSubmit(BaseModel):
    answers: List[Union[str, List[str]]]  # String for list type, List[str] for multiple choice with multiple answers
    completion_time: int

    @validator('answers')
    def validate_answers(cls, v, values, **kwargs):
        # Ensure each answer is either a string or a list of strings
        for answer in v:
            if not isinstance(answer, (str, list)):
                raise ValueError("Each answer must be either a string or a list of strings")
            if isinstance(answer, list):
                if not all(isinstance(a, str) for a in answer):
                    raise ValueError("Multiple choice answers must be strings")
        return v

@router.get("", response_model=List[QuizResponse])
async def list_quizzes(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Quiz)
    if search:
        query = query.filter(Quiz.title.ilike(f"%{search}%"))
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("", response_model=QuizResponse)
async def create_quiz(
    quiz: QuizCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    db_quiz = Quiz(
        creator_id=current_user.id,
        title=quiz.title,
        description=quiz.description,
        quiz_type=quiz.quiz_type,
        time_limit=quiz.time_limit,
        is_multiple_choice=quiz.is_multiple_choice,
        allow_multiple_answers=quiz.allow_multiple_answers
    )
    db.add(db_quiz)
    await db.commit()
    await db.refresh(db_quiz)
    
    # Create answers if provided
    if quiz.answers:
        for answer in quiz.answers:
            db_answer = QuizAnswer(
                quiz_id=db_quiz.id,
                correct_answer=answer.correct_answer,
                aliases=answer.aliases,
                position=answer.position,
                is_correct=answer.is_correct,
                explanation=answer.explanation
            )
            db.add(db_answer)
        await db.commit()
    
    return db_quiz

@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(quiz_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Quiz).filter(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.post("/{quiz_id}/attempts", status_code=status.HTTP_201_CREATED)
async def submit_attempt(
    quiz_id: int,
    attempt: AttemptSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Get quiz and answers
    # Get quiz first
    quiz_result = await db.execute(select(Quiz).filter(Quiz.id == quiz_id))
    quiz = quiz_result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get answers
    answers_result = await db.execute(
        select(QuizAnswer)
        .filter(QuizAnswer.quiz_id == quiz_id)
        .order_by(QuizAnswer.position)
    )
    quiz_answers = answers_result.scalars().all()
    if not quiz_answers:
        raise HTTPException(status_code=400, detail="Quiz has no answers")
    
    # Calculate score
    total_questions = len(quiz_answers)
    correct_answers = 0
    
    # Validate attempt answers length
    if len(attempt.answers) != total_questions:
        raise HTTPException(
            status_code=400,
            detail=f"Expected {total_questions} answers, got {len(attempt.answers)}"
        )
    
    for i, answer in enumerate(quiz_answers):
        if i >= len(attempt.answers):
            break
            
        if quiz.is_multiple_choice:
            # Handle multiple choice answers
            user_answers = attempt.answers[i] if isinstance(attempt.answers[i], list) else [attempt.answers[i]]
            user_answers = [a.lower().strip() for a in user_answers]
            
            if quiz.allow_multiple_answers:
                # All selected answers must be correct and all correct answers must be selected
                correct_options = [a for a in quiz_answers if a.is_correct]
                correct_answers_set = {a.correct_answer.lower().strip() for a in correct_options}
                if set(user_answers) == correct_answers_set:
                    correct_answers += 1
            else:
                # Single answer must match a correct option
                if len(user_answers) == 1 and any(
                    user_answers[0] == a.correct_answer.lower().strip() 
                    for a in quiz_answers if a.is_correct
                ):
                    correct_answers += 1
        else:
            # Handle list type answers
            user_answer = attempt.answers[i].lower().strip() if isinstance(attempt.answers[i], str) else ""
            if (user_answer == answer.correct_answer.lower().strip() or
                (answer.aliases and user_answer in [a.lower().strip() for a in answer.aliases.split(",")])):
                correct_answers += 1
    
    score = int((correct_answers / total_questions) * 100)
    
    # Record attempt
    import json
    db_attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=current_user.id,
        score=score,
        completion_time=attempt.completion_time,
        answers=json.dumps(attempt.answers)
    )
    db.add(db_attempt)
    
    # Update quiz attempt count
    quiz = quiz_answers[0][0]
    quiz.attempt_count += 1
    
    # Update user points (1 point per correct answer)
    current_user.points += correct_answers
    
    await db.commit()
    
    return {
        "score": score,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "points_earned": correct_answers
    }
