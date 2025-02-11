import React, { useState, useEffect } from "react";
import { Button } from "../ui/button";
import { Textarea } from "../ui/textarea";
import { Card, CardContent } from "../ui/card";
import { quizzes, comments, type Comment } from "../../lib/api";
import { formatDistanceToNow } from "date-fns";

interface CommentProps {
  comment: Comment;
  onReply: (commentId: number, content: string) => void;
  onDelete: (commentId: number) => void;
  onUpdate: (commentId: number, content: string) => void;
}

const CommentItem: React.FC<CommentProps> = ({ comment, onReply, onDelete, onUpdate }) => {
  const [isReplying, setIsReplying] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [replyContent, setReplyContent] = useState("");
  const [editContent, setEditContent] = useState(comment.content);

  const handleReplySubmit = () => {
    if (replyContent.trim()) {
      onReply(comment.id, replyContent);
      setReplyContent("");
      setIsReplying(false);
    }
  };

  const handleUpdateSubmit = () => {
    if (editContent.trim() && editContent !== comment.content) {
      onUpdate(comment.id, editContent);
      setIsEditing(false);
    }
  };

  return (
    <Card className="mb-4">
      <CardContent className="pt-4">
        <div className="flex justify-between items-start">
          <div>
            <p className="font-medium">{comment.author_username}</p>
            <p className="text-sm text-muted-foreground">
              {formatDistanceToNow(new Date(comment.created_at), { addSuffix: true })}
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="ghost" size="sm" onClick={() => setIsReplying(!isReplying)}>
              Reply
            </Button>
            <Button variant="ghost" size="sm" onClick={() => setIsEditing(!isEditing)}>
              Edit
            </Button>
            <Button variant="ghost" size="sm" onClick={() => onDelete(comment.id)}>
              Delete
            </Button>
          </div>
        </div>

        {isEditing ? (
          <div className="mt-2 space-y-2">
            <Textarea
              value={editContent}
              onChange={(e) => setEditContent(e.target.value)}
              className="min-h-[100px]"
            />
            <div className="flex gap-2">
              <Button onClick={handleUpdateSubmit}>Save</Button>
              <Button variant="ghost" onClick={() => setIsEditing(false)}>
                Cancel
              </Button>
            </div>
          </div>
        ) : (
          <p className="mt-2">{comment.content}</p>
        )}

        {isReplying && (
          <div className="mt-4 space-y-2">
            <Textarea
              placeholder="Write a reply..."
              value={replyContent}
              onChange={(e) => setReplyContent(e.target.value)}
              className="min-h-[100px]"
            />
            <div className="flex gap-2">
              <Button onClick={handleReplySubmit}>Reply</Button>
              <Button variant="ghost" onClick={() => setIsReplying(false)}>
                Cancel
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

interface CommentSectionProps {
  quizId: number;
}

export function CommentSection({ quizId }: CommentSectionProps) {
  const [commentsList, setCommentsList] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const fetchComments = async () => {
    try {
      const data = await quizzes.getComments(quizId);
      setCommentsList(data);
    } catch (error) {
      console.error("Failed to fetch comments:", error);
    }
  };

  useEffect(() => {
    fetchComments();
  }, [quizId]);

  const handleAddComment = async () => {
    if (!newComment.trim()) return;
    setIsLoading(true);
    try {
      await quizzes.addComment(quizId, newComment);
      setNewComment("");
      await fetchComments();
    } catch (error) {
      console.error("Failed to add comment:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReply = async (commentId: number, content: string) => {
    try {
      await comments.reply(commentId, content);
      await fetchComments();
    } catch (error) {
      console.error("Failed to reply to comment:", error);
    }
  };

  const handleUpdate = async (commentId: number, content: string) => {
    try {
      await comments.update(commentId, content);
      await fetchComments();
    } catch (error) {
      console.error("Failed to update comment:", error);
    }
  };

  const handleDelete = async (commentId: number) => {
    try {
      await comments.delete(commentId);
      await fetchComments();
    } catch (error) {
      console.error("Failed to delete comment:", error);
    }
  };

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Textarea
          placeholder="Write a comment..."
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          className="min-h-[100px]"
        />
        <Button onClick={handleAddComment} disabled={isLoading}>
          {isLoading ? "Adding Comment..." : "Add Comment"}
        </Button>
      </div>

      <div className="space-y-4">
        {commentsList.map((comment) => (
          <CommentItem
            key={comment.id}
            comment={comment}
            onReply={handleReply}
            onDelete={handleDelete}
            onUpdate={handleUpdate}
          />
        ))}
      </div>
    </div>
  );
}
