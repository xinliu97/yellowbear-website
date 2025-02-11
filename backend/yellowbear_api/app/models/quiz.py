from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    quiz_type = Column(String(50), nullable=False)  # list, multiple_choice
    time_limit = Column(Integer)  # in seconds
    attempt_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    is_multiple_choice = Column(Boolean, default=False)  # True for multiple choice quizzes
    allow_multiple_answers = Column(Boolean, default=False)  # True if multiple answers can be selected

    # Relationships
    creator = relationship("User", back_populates="quizzes")
    answers = relationship("QuizAnswer", back_populates="quiz")
    attempts = relationship("QuizAttempt", back_populates="quiz")
    comments = relationship("Comment", back_populates="quiz")
    stats = relationship("QuizStats", back_populates="quiz")

class QuizAnswer(Base):
    __tablename__ = "quiz_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    correct_answer = Column(Text, nullable=False)
    aliases = Column(String)  # JSON array of acceptable alternative answers stored as string
    position = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    is_correct = Column(Boolean, default=False)  # For multiple choice: whether this option is correct
    explanation = Column(Text)  # Optional explanation for why this answer is correct/incorrect

    # Relationships
    quiz = relationship("Quiz", back_populates="answers")
    stats = relationship("QuizStats", back_populates="answer")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, nullable=False)
    completion_time = Column(Integer)  # Time taken in seconds
    answers = Column(String)  # JSON array of user answers stored as string
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User", back_populates="quiz_attempts")
