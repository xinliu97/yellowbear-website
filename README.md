# YellowBear Quiz Platform | 黄熊测验平台

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

### Overview
YellowBear Quiz is an interactive quiz platform inspired by Sporcle, featuring modern UI design and mobile-first responsive layout. The platform supports multiple quiz types, user authentication, and social features.

### Project Structure
```
yellowbear-website/
├── frontend/           # React frontend application
│   └── yellowbear_web/
└── backend/           # FastAPI backend service
    └── yellowbear_api/
```

### Frontend Development

> Note for Frontend Developers: You only need to focus on the frontend implementation. The backend API endpoints are documented in the API Documentation section, and you only need to configure the backend URL in your environment variables.

#### Tech Stack
- React with TypeScript
- Tailwind CSS for styling
- React Router for navigation
- Axios for API requests

#### Setup Instructions
1. Navigate to frontend directory:
```bash
cd frontend/yellowbear_web
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
Create `.env` file with:
```env
VITE_API_URL=https://your-backend-url
```

4. Start development server:
```bash
npm run dev
```

#### API Configuration
- Update `VITE_API_URL` in `.env` to point to your backend server
  ```env
  # For development with local backend
  VITE_API_URL=http://localhost:8000

  # For production backend
  VITE_API_URL=https://app-pvtpokib.fly.dev
  ```
- All API endpoints are configured in `src/lib/api.ts`
- Authentication tokens are managed automatically via Axios interceptors
- When deploying to production, ensure you're using the production backend URL

### Backend Development

> Note for Backend Developers: You only need to focus on implementing the API endpoints according to the specifications. Frontend teams will interact with your API through documented endpoints. You don't need to worry about how the frontend implements these features.

#### Tech Stack
- FastAPI
- SQLAlchemy for ORM
- PostgreSQL database
- JWT authentication

#### Setup Instructions
1. Navigate to backend directory:
```bash
cd backend/yellowbear_api
```

2. Install dependencies:
```bash
poetry install
```

3. Configure environment:
Create `.env` file with:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/yellowbear
JWT_SECRET=your-secret-key
WECHAT_APP_ID=your-wechat-app-id
WECHAT_APP_SECRET=your-wechat-app-secret
WEIBO_CLIENT_ID=your-weibo-client-id
WEIBO_CLIENT_SECRET=your-weibo-client-secret
```

4. Start development server:
```bash
poetry run uvicorn app.main:app --reload
```

#### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Interface
The frontend and backend teams communicate through well-defined REST API endpoints. Backend developers implement these endpoints according to the API documentation, while frontend developers consume them. This separation allows both teams to work independently as long as they adhere to the agreed-upon API contract.

---

<a name="chinese"></a>
## 中文

### 项目概述
黄熊测验平台是一个受 Sporcle 启发的互动测验平台，具有现代化的用户界面设计和移动优先的响应式布局。平台支持多种测验类型、用户认证和社交功能。

### 项目结构
```
yellowbear-website/
├── frontend/           # React 前端应用
│   └── yellowbear_web/
└── backend/           # FastAPI 后端服务
    └── yellowbear_api/
```

### 前端开发

> 前端开发者注意：您只需要关注前端实现。后端 API 端点在 API 文档部分有详细说明，您只需要在环境变量中配置后端 URL 即可。

#### 技术栈
- React 配合 TypeScript
- Tailwind CSS 用于样式设计
- React Router 用于导航
- Axios 用于 API 请求

#### 环境配置
1. 进入前端目录：
```bash
cd frontend/yellowbear_web
```

2. 安装依赖：
```bash
npm install
```

3. 配置环境变量：
创建 `.env` 文件并添加：
```env
VITE_API_URL=https://你的后端地址
```

4. 启动开发服务器：
```bash
npm run dev
```

#### API 配置
- 在 `.env` 文件中更新 `VITE_API_URL` 指向你的后端服务器
  ```env
  # 用于本地开发环境
  VITE_API_URL=http://localhost:8000

  # 用于生产环境
  VITE_API_URL=https://app-pvtpokib.fly.dev
  ```
- 所有 API 端点配置都在 `src/lib/api.ts` 中
- 认证令牌通过 Axios 拦截器自动管理
- 部署到生产环境时，确保使用生产环境的后端 URL

### 后端开发

> 后端开发者注意：您只需要专注于按照规范实现 API 端点。前端团队将通过文档化的端点与您的 API 交互。您无需关心前端如何实现这些功能。

#### 技术栈
- FastAPI
- SQLAlchemy ORM
- PostgreSQL 数据库
- JWT 认证

#### 环境配置
1. 进入后端目录：
```bash
cd backend/yellowbear_api
```

2. 安装依赖：
```bash
poetry install
```

3. 配置环境变量：
创建 `.env` 文件并添加：
```env
DATABASE_URL=postgresql://user:password@localhost:5432/yellowbear
JWT_SECRET=你的密钥
WECHAT_APP_ID=你的微信应用ID
WECHAT_APP_SECRET=你的微信应用密钥
WEIBO_CLIENT_ID=你的微博客户端ID
WEIBO_CLIENT_SECRET=你的微博客户端密钥
```

4. 启动开发服务器：
```bash
poetry run uvicorn app.main:app --reload
```

#### API 文档
- Swagger UI：`http://localhost:8000/docs`
- ReDoc：`http://localhost:8000/redoc`

### API 接口
前端和后端团队通过明确定义的 REST API 端点进行通信。后端开发者根据 API 文档实现这些端点，而前端开发者则调用这些端点。这种分离允许两个团队独立工作，只要他们遵守约定的 API 契约即可。
