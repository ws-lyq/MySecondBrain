# EnglishMagazineSystem · 英语外刊管理系统 - 架构分析

## 项目概览

| 项目 | 内容 |
|------|------|
| **路径** | `C:\Users\lyq29\Desktop\EnglishMagazineSystem` |
| **语言** | Java 17+ |
| **构建** | Maven (pom.xml) |
| **数据库** | MySQL 8.0 |
| **GUI** | Java Swing |
| **外部API** | DeepSeek AI 生成文章 |
| **包名** | `com.englishmagazine` |
| **GitHub** | https://github.com/ws-lyq/EnglishMagzineSystem |

## 技术栈

| Layer | Technology |
|-------|-----------|
| Language | Java 17+ |
| GUI | Java Swing |
| Build | Maven |
| Database | MySQL 8.0 |
| AI API | DeepSeek Chat |
| Auth | jBCrypt (未启用，当前用明文) |

## 项目结构

```
src/main/java/com/englishmagazine/
├── Main.java                    # 入口：设置Swing外观，启动LoginFrame
├── model/                       # 实体层
│   ├── Article.java             # 文章（标题/中英文内容/难度/分类/关联用户）
│   ├── User.java                # 用户（用户名/密码/邮箱/角色admin或user）
│   ├── Vocabulary.java          # 单词（拼写/音标/词性/释义/例句）
│   └── UserVocabulary.java      # 用户-单词关联（含冗余的单词详细信息）
├── dao/                         # 数据访问层（接口 + JDBC实现）
│   ├── ArticleDAO / Impl        # 文章CRUD + 按难度/分类/用户筛选
│   ├── UserDAO / Impl           # 用户认证/CRUD + 用户名查重
│   ├── VocabularyDAO / Impl     # 单词CRUD + 模糊搜索 + 批量导入
│   └── UserVocabularyDAO / Impl # 生词本增删查 + 查重 + 统计
├── service/                     # 业务逻辑层
│   ├── ArticleService.java      # 文章业务 + AI生成文章（DeepSeek API）
│   ├── UserService.java         # 登录注册/用户管理（含JDBC绕开DAO的搜索方法）
│   ├── VocabularyService.java   # 单词管理 + 词性统计
│   └── UserVocabularyService.java # 生词本管理
├── ui/                          # Swing视图层
│   ├── LoginFrame.java          # 登录/注册（CardLayout切换，渐变背景）
│   ├── AdminFrame.java          # 管理员控制台（用户/文章/单词管理Tab，1300+行）
│   ├── UserMainFrame.java       # 普通用户界面（阅读/查词/生词本/个人中心，1370+行）
│   └── RegisterDialog.java      # 注册对话框
└── util/                        # 工具层
    ├── DatabaseUtil.java        # MySQL连接管理（db.properties配置）
    ├── AIService.java           # DeepSeek API调用（手动JSON解析响应）
    └── PasswordUtil.java        # 明文密码处理（课程演示用）
```

## 核心数据流

```
Main → LoginFrame → 用户登录
    ├── admin → AdminFrame（用户管理 / 文章管理 / 单词管理）
    └── user  → UserMainFrame（文章阅读 / 单词查询 / 生词本 / 个人中心）
                        ↓
                   Service 层（业务逻辑 + AI调用）
                        ↓
                    DAO 层（JDBC）
                        ↓
                     MySQL 数据库
                        ↑
              AIService ← DeepSeek API（根据生词本AI生成文章）
```

## 关键业务流程

### 1. 用户登录与角色路由
```
LoginFrame.performLogin()
    → UserService.login()
        → UserDAO.authenticate()
    → 根据 role 字段：
        "admin" → AdminFrame
        "user"  → UserMainFrame
```

### 2. AI 生成文章
```
UserMainFrame → ArticleService.generateAndSaveArticleFromWords()
    → UserVocabularyService.getUserVocabularyWords()  # 取用户生词
    → AIService.generateArticle()                      # 调DeepSeek API
    → 解析返回的 JSON，提取英文内容 + 中文翻译
    → 创建 Article 对象并调用 DAO 存入数据库
```

### 3. 生词本管理
```
单词查询 → 加入生词本 → UserVocabularyService.addVocabularyToUser()
    → UserVocabularyDAO.addVocabularyToUser()
    → 检查是否已存在（防重复）
生词本列表 → 支持搜索/移除/清空
单词复习 → 弹出对话框显示所有生词
单词测试 → 检查生词数量是否≥5
```

## 数据库表结构

### users 表
- user_id (INT, PK)
- username (VARCHAR)
- password (VARCHAR, 当前明文)
- email (VARCHAR)
- role (VARCHAR: 'admin'/'user')
- created_at (TIMESTAMP)

### articles 表
- article_id (INT, PK)
- title (VARCHAR)
- english_content (TEXT)
- chinese_translation (TEXT)
- difficulty (VARCHAR: 'easy'/'medium'/'hard')
- category (VARCHAR)
- publish_date (DATE)
- word_count (INT)
- created_at (TIMESTAMP)
- user_id (INT, FK → users)

### vocabulary 表
- word_id (INT, PK)
- word (VARCHAR)
- phonetic (VARCHAR)
- part_of_speech (VARCHAR)
- translation (VARCHAR)
- example_sentence (TEXT)

### user_vocabulary 表
- user_vocab_id (INT, PK)
- user_id (INT, FK → users)
- word_id (INT, FK → vocabulary)
- added_date (TIMESTAMP)

## 架构模式：分层架构 (Layered Architecture)

```
┌─────────────────────────────────────────────────────┐
│  UI 层 (ui)           Java Swing JFrame             │
│  LoginFrame / AdminFrame / UserMainFrame             │
├─────────────────────────────────────────────────────┤
│  Service 层 (service)  业务逻辑编排                   │
│  ArticleService / UserService / ...                  │
├─────────────────────────────────────────────────────┤
│  DAO 层 (dao)         接口 + JDBC实现                │
│  *DAO (interface) → *DAOImpl (MySQL)                  │
├─────────────────────────────────────────────────────┤
│  Model 层 (model)      POJO 实体类                   │
│  Article / User / Vocabulary / UserVocabulary        │
└─────────────────────────────────────────────────────┘
        ┌──────────────────────────┐
        │  Util 层 (util)          │
        │  DatabaseUtil / AIService │
        └──────────────────────────┘
```

## 已知待改进

- [ ] 密码加密（jBCrypt 已引入但未使用）
- [ ] API Key 从版本控制移除（已完成）
- [ ] DAO 层 try-with-resources 统一
- [ ] 拆分超大 UI 类（AdminFrame 1300+行、UserMainFrame 1370+行）
- [ ] 引入连接池（HikariCP）
- [ ] 用日志框架替换 e.printStackTrace()
- [ ] 删除用户时级联删除关联的文章和生词本
- [ ] 修改密码功能未实现
- [ ] 单词"已掌握"标记未实现
