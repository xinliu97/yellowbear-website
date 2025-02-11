
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { quizzes } from "@/lib/api";

interface Answer {
  correct_answer: string;
  aliases: string[];
  position: number;
}

export function CreateQuizPage() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [timeLimit, setTimeLimit] = useState<number>(0);
  const [answers, setAnswers] = useState<Answer[]>([{ correct_answer: "", aliases: [], position: 0 }]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await quizzes.create({
        title,
        description,
        quiz_type: "standard",
        time_limit: timeLimit,
        answers,
      });
      navigate("/quizzes");
    } catch (error) {
      console.error("Failed to create quiz:", error);
    }
  };

  const addAnswer = () => {
    setAnswers([...answers, { correct_answer: "", aliases: [], position: answers.length }]);
  };

  const updateAnswer = (index: number, value: string) => {
    const newAnswers = [...answers];
    newAnswers[index].correct_answer = value;
    setAnswers(newAnswers);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>Create New Quiz</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Input
                placeholder="Quiz Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>
            <div>
              <Input
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>
            <div>
              <Input
                type="number"
                placeholder="Time Limit (seconds)"
                value={timeLimit}
                onChange={(e) => setTimeLimit(parseInt(e.target.value))}
              />
            </div>
            <div className="space-y-4">
              {answers.map((answer, index) => (
                <div key={index}>
                  <Input
                    placeholder={`Answer ${index + 1}`}
                    value={answer.correct_answer}
                    onChange={(e) => updateAnswer(index, e.target.value)}
                    required
                  />
                </div>
              ))}
              <Button type="button" variant="outline" onClick={addAnswer}>
                Add Answer
              </Button>
            </div>
            <Button type="submit">Create Quiz</Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
