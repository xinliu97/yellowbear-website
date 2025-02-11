from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    points = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    quizzes = relationship("Quiz", back_populates="creator")
    comments = relationship("Comment", back_populates="author")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
