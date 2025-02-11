import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from ..app.models import Quiz, QuizAnswer, User
from ..app.database import get_db
from ..app.main import app

@pytest.fixture
async def test_user(db: AsyncSession):
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        points=0
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@pytest.fixture
async def test_quiz(db: AsyncSession, test_user: User):
    quiz = Quiz(
        creator_id=test_user.id,
        title="Test Quiz",
        description="Test Description",
        quiz_type="multiple_choice",
        time_limit=300,
        is_multiple_choice=True,
        allow_multiple_answers=True
    )
    db.add(quiz)
    await db.commit()
    await db.refresh(quiz)
    
    # Add answers
    answers = [
        QuizAnswer(
            quiz_id=quiz.id,
            correct_answer="Paris",
            aliases=["paris"],
            position=0,
            is_correct=True,
            explanation="Capital of France"
        ),
        QuizAnswer(
            quiz_id=quiz.id,
            correct_answer="London",
            aliases=["london"],
            position=1,
            is_correct=True,
            explanation="Capital of UK"
        ),
        QuizAnswer(
            quiz_id=quiz.id,
            correct_answer="Berlin",
            aliases=["berlin"],
            position=2,
            is_correct=False,
            explanation="Not a correct answer"
        )
    ]
    for answer in answers:
        db.add(answer)
    await db.commit()
    return quiz

@pytest.mark.asyncio
async def test_create_quiz(client: AsyncClient, test_user: User):
    response = await client.post(
        "/api/quizzes",
        json={
            "title": "New Quiz",
            "description": "Test Quiz",
            "quiz_type": "multiple_choice",
            "time_limit": 300,
            "is_multiple_choice": True,
            "allow_multiple_answers": True,
            "answers": [
                {
                    "correct_answer": "Paris",
                    "aliases": ["paris"],
                    "position": 0,
                    "is_correct": True,
                    "explanation": "Capital of France"
                },
                {
                    "correct_answer": "London",
                    "aliases": ["london"],
                    "position": 1,
                    "is_correct": True,
                    "explanation": "Capital of UK"
                }
            ]
        },
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Quiz"
    assert data["quiz_type"] == "multiple_choice"
    assert data["is_multiple_choice"] is True

@pytest.mark.asyncio
async def test_submit_multiple_choice_attempt(client: AsyncClient, test_quiz: Quiz, test_user: User):
    response = await client.post(
        f"/api/quizzes/{test_quiz.id}/attempts",
        json={
            "answers": [["Paris", "London"], [], ["Berlin"]],
            "completion_time": 120
        },
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 66  # 2 out of 3 correct
    assert data["correct_answers"] == 2
    assert data["total_questions"] == 3

@pytest.mark.asyncio
async def test_get_quiz_statistics(client: AsyncClient, test_quiz: Quiz):
    response = await client.get(f"/api/stats/quizzes/{test_quiz.id}")
    assert response.status_code == 200
    data = response.json()
    assert "total_attempts" in data
    assert "average_score" in data
    assert "answers_stats" in data
    assert len(data["answers_stats"]) == 3
