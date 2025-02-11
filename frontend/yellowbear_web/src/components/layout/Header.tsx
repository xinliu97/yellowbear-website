import { Button } from "@/components/ui/button";
import { useNavigate, Link } from "react-router-dom";
import { Menu } from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from "@/components/ui/sheet";

export function Header() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 flex">
          <Link to="/" className="mr-6 flex items-center space-x-2">
            <span className="font-bold">YellowBear Quiz</span>
          </Link>
          <nav className="hidden md:flex items-center space-x-6 text-sm font-medium">
            <Link to="/quizzes" className="transition-colors hover:text-foreground/80">
              Quizzes
            </Link>
            {token && (
              <Link to="/quizzes/new" className="transition-colors hover:text-foreground/80">
                Create Quiz
              </Link>
            )}
          </nav>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <div className="w-full flex-1 md:w-auto md:flex-none">
            {/* Search functionality will be added later */}
          </div>
          <nav className="flex items-center space-x-4">
            {token ? (
              <>
                <div className="text-sm">
                  <span className="text-muted-foreground">Points: </span>
                  <span className="font-medium">{localStorage.getItem('userPoints') || 0}</span>
                </div>
                <Button variant="ghost" onClick={handleLogout}>
                  Logout
                </Button>
              </>
            ) : (
              <div className="hidden md:flex space-x-2">
                <Button variant="ghost" onClick={() => navigate('/login')}>
                  Login
                </Button>
                <Button onClick={() => navigate('/register')}>
                  Sign Up
                </Button>
                <Button variant="outline" onClick={() => window.location.href = `${import.meta.env.VITE_API_URL}/api/auth/wechat`}>
                  WeChat Login
                </Button>
                <Button variant="outline" onClick={() => window.location.href = `${import.meta.env.VITE_API_URL}/api/auth/weibo`}>
                  Weibo Login
                </Button>
              </div>
            )}
            <Sheet>
              <SheetTrigger asChild className="md:hidden">
                <Button variant="ghost" size="icon">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-[250px]">
                <nav className="flex flex-col space-y-4">
                  <Link to="/quizzes" className="text-sm font-medium">
                    Quizzes
                  </Link>
                  {token && (
                    <Link to="/quizzes/new" className="text-sm font-medium">
                      Create Quiz
                    </Link>
                  )}
                  {token ? (
                    <Button variant="ghost" onClick={handleLogout}>
                      Logout
                    </Button>
                  ) : (
                    <>
                      <Button variant="ghost" onClick={() => navigate('/login')}>
                        Login
                      </Button>
                      <Button onClick={() => navigate('/register')}>
                        Sign Up
                      </Button>
                    </>
                  )}
                </nav>
              </SheetContent>
            </Sheet>
          </nav>
        </div>
      </div>
    </header>
  );
}
