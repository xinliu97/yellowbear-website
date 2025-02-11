# YellowBear Quiz Platform Technical Specification

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    oauth_id VARCHAR(255),
    oauth_provider VARCHAR(50),
    points INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Quizzes Table
```sql
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    quiz_type VARCHAR(50) NOT NULL,
    tags TEXT[], -- Array of tags
    time_limit INTEGER, -- In seconds
    attempt_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### QuizAnswers Table
```sql
CREATE TABLE quiz_answers (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizzes(id),
    correct_answer TEXT NOT NULL,
    aliases TEXT[], -- Array of acceptable alternative answers
    position INTEGER NOT NULL, -- Order in the quiz
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### QuizAttempts Table
```sql
CREATE TABLE quiz_attempts (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizzes(id),
    user_id INTEGER REFERENCES users(id),
    score INTEGER NOT NULL,
    completion_time INTEGER, -- Time taken in seconds
    answers JSONB, -- Stores detailed answer history
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### QuizStats Table
```sql
CREATE TABLE quiz_stats (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizzes(id),
    answer_id INTEGER REFERENCES quiz_answers(id),
    correct_count INTEGER DEFAULT 0,
    attempt_count INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Comments Table
```sql
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizzes(id),
    user_id INTEGER REFERENCES users(id),
    parent_id INTEGER REFERENCES comments(id),
    content TEXT NOT NULL,
    likes_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Authentication
```
POST /api/register
- Request: { username, email, password }
- Response: { user_id, token }

POST /api/login
- Request: { email, password }
- Response: { user_id, token }

GET /api/profile
- Headers: Authorization: Bearer {token}
- Response: { user_id, username, email, points, created_at }

PUT /api/profile
- Headers: Authorization: Bearer {token}
- Request: { username, email }
- Response: { user_id, username, email, points }
```

### Quiz Management
```
GET /api/quizzes
- Query: { page, limit, search, tags }
- Response: { quizzes: [...], total, page }

GET /api/quizzes/{id}
- Response: { quiz_details, creator, stats }

POST /api/quizzes
- Headers: Authorization: Bearer {token}
- Request: { title, description, type, tags, time_limit, answers: [...] }
- Response: { quiz_id }

PUT /api/quizzes/{id}
- Headers: Authorization: Bearer {token}
- Request: { title, description, type, tags, time_limit, answers: [...] }
- Response: { quiz_id }

DELETE /api/quizzes/{id}
- Headers: Authorization: Bearer {token}
- Response: { success: true }
```

### Quiz Attempts & Statistics
```
POST /api/quizzes/{id}/attempts
- Headers: Authorization: Bearer {token}
- Request: { answers: [...], completion_time }
- Response: { score, correct_answers, stats }

GET /api/quizzes/{id}/stats
- Response: { attempt_count, avg_score, answer_stats: [...] }
```

### Comments
```
GET /api/quizzes/{id}/comments
- Query: { page, limit }
- Response: { comments: [...], total, page }

POST /api/quizzes/{id}/comments
- Headers: Authorization: Bearer {token}
- Request: { content, parent_id? }
- Response: { comment_id }

POST /api/comments/{id}/replies
- Headers: Authorization: Bearer {token}
- Request: { content }
- Response: { comment_id }

PUT /api/comments/{id}
- Headers: Authorization: Bearer {token}
- Request: { content }
- Response: { comment_id }

DELETE /api/comments/{id}
- Headers: Authorization: Bearer {token}
- Response: { success: true }
```

### Leaderboard & Achievements
```
GET /api/leaderboard
- Query: { timeframe, page, limit }
- Response: { rankings: [...], total, page }

GET /api/users/{id}/achievements
- Response: { points, achievements: [...] }
```

## Frontend Routes

- `/` - Home page with featured quizzes
- `/login` - Login page
- `/register` - Registration page
- `/profile` - User profile page
- `/quizzes` - Quiz listing page
- `/quizzes/new` - Create new quiz
- `/quizzes/:id` - Quiz detail/play page
- `/quizzes/:id/stats` - Quiz statistics page
- `/leaderboard` - Global leaderboard
