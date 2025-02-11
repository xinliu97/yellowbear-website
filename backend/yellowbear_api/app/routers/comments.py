from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from pydantic import BaseModel
from .. import models, database
from ..auth import get_current_user

router = APIRouter()

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    author_id: int
    quiz_id: int
    parent_id: Optional[int]
    created_at: str
    updated_at: str
    likes_count: int
    author_username: str

    class Config:
        from_attributes = True

@router.get("/api/quizzes/{quiz_id}/comments", response_model=List[CommentResponse])
async def get_quiz_comments(
    quiz_id: int,
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(models.Comment).where(
            models.Comment.quiz_id == quiz_id,
            models.Comment.is_deleted == False
        )
    )
    comments = result.scalars().all()
    return comments

@router.post("/api/quizzes/{quiz_id}/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(
    quiz_id: int,
    comment: CommentCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_comment = models.Comment(
        content=comment.content,
        quiz_id=quiz_id,
        author_id=current_user.id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    
    # Award points for commenting
    current_user.points += 1
    await db.commit()
    
    return db_comment

@router.post("/api/comments/{comment_id}/replies", status_code=status.HTTP_201_CREATED)
async def create_reply(
    comment_id: int,
    reply: CommentCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Comment).where(models.Comment.id == comment_id)
    )
    parent_comment = result.scalar_one_or_none()
    if not parent_comment:
        raise HTTPException(status_code=404, detail="Parent comment not found")
    
    db_reply = models.Comment(
        content=reply.content,
        quiz_id=parent_comment.quiz_id,
        author_id=current_user.id,
        parent_id=comment_id
    )
    db.add(db_reply)
    await db.commit()
    await db.refresh(db_reply)
    
    # Award points for replying
    current_user.points += 1
    await db.commit()
    
    return db_reply

@router.put("/api/comments/{comment_id}")
async def update_comment(
    comment_id: int,
    comment: CommentCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Comment).where(models.Comment.id == comment_id)
    )
    db_comment = result.scalar_one_or_none()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if db_comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    
    db_comment.content = comment.content
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

@router.delete("/api/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    result = await db.execute(
        select(models.Comment).where(models.Comment.id == comment_id)
    )
    db_comment = result.scalar_one_or_none()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if db_comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db_comment.is_deleted = True
    await db.commit()
    return {"message": "Comment deleted successfully"}
