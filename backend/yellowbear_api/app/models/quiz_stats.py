from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class QuizStats(Base):
    __tablename__ = "quiz_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    answer_id = Column(Integer, ForeignKey("quiz_answers.id"))
    correct_count = Column(Integer, default=0)
    attempt_count = Column(Integer, default=0)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    quiz = relationship("Quiz", back_populates="stats")
    answer = relationship("QuizAnswer", back_populates="stats")
