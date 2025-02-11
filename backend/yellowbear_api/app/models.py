from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, JSON, func, Boolean
from sqlalchemy.orm import relationship
from .models.base import Base

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

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    quiz_type = Column(String(50), nullable=False)
    time_limit = Column(Integer)  # in seconds
    attempt_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())

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
    aliases = Column(JSON)  # Array of acceptable alternative answers
    position = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

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
    answers = Column(JSON)  # Stores detailed answer history
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User", back_populates="quiz_attempts")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    likes_count = Column(Integer, default=0)

    # Relationships
    quiz = relationship("Quiz", back_populates="comments")
    author = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")
