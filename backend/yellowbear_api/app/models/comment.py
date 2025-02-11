from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP, JSON, func, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

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
