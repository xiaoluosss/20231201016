# Veaury贴吧项目

一个基于Vue.js + React混合技术栈的现代化贴吧系统，采用前后端分离架构。

## 🚀 项目特色

- **混合技术栈**: Vue.js + React 混合开发
- **现代化UI**: 响应式设计，支持移动端和桌面端
- **完整功能**: 贴吧创建、帖子发布、评论互动、用户管理
- **RESTful API**: 基于Django REST Framework的完整API
- **实时交互**: 支持点赞、收藏、关注等社交功能

## 📋 功能模块

### 后端功能 (Django + DRF)
- ✅ 用户认证与权限管理
- ✅ 贴吧分类与管理
- ✅ 帖子发布与浏览
- ✅ 评论与回复系统
- ✅ 点赞、收藏、关注功能
- ✅ 文件上传支持
- ✅ 搜索功能

### 前端功能 (Vue.js + React)
- ✅ 响应式用户界面
- ✅ 贴吧浏览与搜索
- ✅ 帖子发布与编辑
- ✅ 实时评论互动
- ✅ 用户个人中心
- ✅ 消息通知系统

## 🛠️ 技术栈

### 后端技术
- **框架**: Django 4.2
- **API**: Django REST Framework 3.14
- **数据库**: SQLite (开发) / MySQL (生产)
- **认证**: Session + Token认证
- **缓存**: Redis
- **任务队列**: Celery

### 前端技术
- **框架**: Vue.js 3 + React 18
- **构建工具**: Vite
- **状态管理**: Pinia + Redux
- **路由**: Vue Router + React Router
- **UI组件**: Element Plus + Ant Design
- **HTTP客户端**: Axios

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- Redis (可选)
- MySQL (生产环境)

### 后端启动
```bash
# 克隆项目
git clone <repository-url>
cd veaury-tieba

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
cd backend
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

### 前端启动
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📁 项目结构

```
veaury-tieba/
├── backend/                 # Django后端
│   ├── config/             # 项目配置
│   ├── users/              # 用户应用
│   ├── tiebas/             # 贴吧应用
│   ├── posts/              # 帖子应用
│   ├── comments/           # 评论应用
│   └── templates/          # 模板文件
├── frontend/               # 前端项目
│   ├── src/
│   │   ├── vue-components/ # Vue组件
│   │   ├── services/       # API服务
│   │   ├── stores/         # 状态管理
│   │   └── router/         # 路由配置
│   └── vite.config.js      # Vite配置
└── docs/                   # 项目文档
```

## 🔧 配置说明

### 环境变量
创建 `.env` 文件：
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

### API端点
- 用户API: `/api/auth/`
- 贴吧API: `/api/tiebas/`
- 帖子API: `/api/posts/`
- 评论API: `/api/comments/`

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 项目主页: [GitHub Repository]
- 问题反馈: [Issues]
- 邮箱: your-email@example.com

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！