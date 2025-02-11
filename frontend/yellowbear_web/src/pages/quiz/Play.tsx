import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert } from "@/components/ui/alert";
import { quizzes } from "@/lib/api";
import type { Quiz } from "@/lib/api";
import { CommentSection } from "@/components/comments/CommentSection";

export function PlayQuizPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [answers, setAnswers] = useState<string[]>([]);
  const [currentAnswer, setCurrentAnswer] = useState("");
  const [timeLeft, setTimeLeft] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [result, setResult] = useState<{
    score: number;
    correct_answers: number;
    total_questions: number;
    points_earned: number;
  } | null>(null);

  useEffect(() => {
    const loadQuiz = async () => {
      try {
        if (!id) return;
        const quizData = await quizzes.get(parseInt(id));
        setQuiz(quizData);
        if (quizData.time_limit) {
          setTimeLeft(quizData.time_limit);
        }
      } catch (err) {
        setError("Failed to load quiz");
      }
    };
    loadQuiz();
  }, [id]);

  useEffect(() => {
    if (timeLeft === null || timeLeft <= 0) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => (prev ? prev - 1 : null));
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

  const handleSubmitAnswer = () => {
    if (!currentAnswer.trim()) return;
    setAnswers([...answers, currentAnswer.trim()]);
    setCurrentAnswer("");
  };

  const handleFinishQuiz = async () => {
    if (!quiz || !id) return;
    try {
      const result = await quizzes.submitAttempt(parseInt(id), {
        answers,
        completion_time: quiz.time_limit ? quiz.time_limit - (timeLeft || 0) : 0,
      });
      setResult(result);
    } catch (err) {
      setError("Failed to submit quiz");
    }
  };

  if (!quiz) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Alert>{error || "Loading quiz..."}</Alert>
      </div>
    );
  }

  if (result) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Quiz Results</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <p className="text-2xl font-bold">Score: {result.score}%</p>
              <p>
                Correct Answers: {result.correct_answers} / {result.total_questions}
              </p>
              <p>Points Earned: {result.points_earned}</p>
              <Button onClick={() => navigate("/quizzes")}>Back to Quizzes</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>{quiz.title}</CardTitle>
          {timeLeft !== null && (
            <p className="text-sm text-muted-foreground">
              Time Left: {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, "0")}
            </p>
          )}
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex space-x-2">
              <Input
                value={currentAnswer}
                onChange={(e) => setCurrentAnswer(e.target.value)}
                placeholder="Enter your answer"
                onKeyPress={(e) => e.key === "Enter" && handleSubmitAnswer()}
              />
              <Button onClick={handleSubmitAnswer}>Submit Answer</Button>
            </div>
            <div className="space-y-2">
              {answers.map((answer, index) => (
                <div key={index} className="p-2 bg-muted rounded">
                  Answer {index + 1}: {answer}
                </div>
              ))}
            </div>
            {answers.length > 0 && (
              <Button onClick={handleFinishQuiz}>Finish Quiz</Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Comments Section */}
      <div className="mt-8">
        <h2 className="text-2xl font-bold mb-4">Comments</h2>
        <CommentSection quizId={parseInt(id || "0")} />
      </div>
    </div>
  );
}
