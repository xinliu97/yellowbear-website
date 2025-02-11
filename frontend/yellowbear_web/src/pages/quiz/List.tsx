
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { quizzes } from "@/lib/api";
import type { Quiz } from "@/lib/api";

export function QuizListPage() {
  const navigate = useNavigate();
  const [quizList, setQuizList] = useState<Quiz[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const data = await quizzes.list();
        setQuizList(data);
      } catch (error) {
        console.error("Failed to fetch quizzes:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuizzes();
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Available Quizzes</h1>
        <Button onClick={() => navigate("/quizzes/new")}>Create Quiz</Button>
      </div>
      
      {loading ? (
        <div>Loading quizzes...</div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {quizList.map((quiz) => (
            <Card key={quiz.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>{quiz.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">
                  {quiz.description || "No description available"}
                </p>
                <div className="flex justify-between items-center">
                  <span className="text-sm">
                    Attempts: {quiz.attempt_count}
                  </span>
                  <Button onClick={() => navigate(`/quizzes/${quiz.id}`)}>
                    Start Quiz
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
