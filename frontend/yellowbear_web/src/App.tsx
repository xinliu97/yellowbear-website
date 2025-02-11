
import { HashRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Header } from "./components/layout/Header";
import { LoginPage } from "./pages/auth/Login";
import { RegisterPage } from "./pages/auth/Register";
import { CreateQuizPage } from "./pages/quiz/Create";
import { PlayQuizPage } from "./pages/quiz/Play";
import { QuizListPage } from "./pages/quiz/List";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";

function App() {
  return (
    <Router basename="/">
      <div className="min-h-screen bg-background">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Navigate to="/quizzes" replace />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route
              path="/quizzes"
              element={
                <ProtectedRoute>
                  <QuizListPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/quizzes/new"
              element={
                <ProtectedRoute>
                  <CreateQuizPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/quizzes/:id"
              element={
                <ProtectedRoute>
                  <PlayQuizPage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
