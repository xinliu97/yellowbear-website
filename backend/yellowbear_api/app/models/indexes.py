from sqlalchemy import Index
from .quiz import Quiz, QuizAnswer, QuizAttempt
from .comment import Comment
from .quiz_stats import QuizStats

# Quiz indexes
Index('idx_quiz_creator', Quiz.creator_id)
Index('idx_quiz_type', Quiz.quiz_type)
Index('idx_quiz_title', Quiz.title)

# Answer indexes
Index('idx_answer_quiz', QuizAnswer.quiz_id)
Index('idx_answer_position', QuizAnswer.position)

# Attempt indexes
Index('idx_attempt_quiz', QuizAttempt.quiz_id)
Index('idx_attempt_user', QuizAttempt.user_id)
Index('idx_attempt_score', QuizAttempt.score)

# Comment indexes
Index('idx_comment_quiz', Comment.quiz_id)
Index('idx_comment_author', Comment.author_id)
Index('idx_comment_parent', Comment.parent_id)
Index('idx_comment_created', Comment.created_at)

# Stats indexes
Index('idx_stats_quiz', QuizStats.quiz_id)
Index('idx_stats_answer', QuizStats.answer_id)
Index('idx_stats_attempts', QuizStats.attempt_count)
