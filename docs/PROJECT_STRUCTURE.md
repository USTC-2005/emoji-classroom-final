# 表情符号课堂项目结构说明

本文档基于当前仓库代码和 `docs/TEAM_MODULES.md` 整理。仓库是在 Vue FastAPI Admin 基础上扩展情绪课堂业务：现有用户、角色、菜单、API、部门和审计日志属于基础管理能力；课程、课堂会话、Emoji 记录、统计看板和 AI 接入目前仍有多个 TODO，占位路由不会自动产生完整业务能力。

## 1. 总体架构

```text
浏览器
  ├─ Vue 3 + Vite + Naive UI
  │    ├─ router：基础路由 + 登录后动态路由
  │    ├─ store：用户、权限、菜单状态
  │    ├─ api：统一封装后端请求
  │    └─ views/components：页面和可复用组件
  │
  └─ HTTP / JSON
       │ 统一前缀：/api/v1
       ▼
FastAPI
  ├─ app/__init__.py：创建应用、注册中间件/异常/路由
  ├─ app/api/v1：按业务模块组织 REST 路由
  ├─ app/controllers：复用 CRUD 和业务规则
  ├─ app/schemas：请求校验与响应结构
  ├─ app/models：Tortoise ORM 数据模型
  ├─ app/services：统计、导出、AI 等跨接口业务
  └─ app/core：认证、权限、数据库初始化、通用 CRUD
       │
       ▼
SQLite（可切换 MySQL/PostgreSQL 等）
```

## 2. 后端目录

### `app/__init__.py` 和 `run.py`

`run.py` 是本地启动入口，使用 Uvicorn 监听 9999 端口。`app/__init__.py` 创建 FastAPI 实例：

1. 创建应用并加载配置。
2. 注册 CORS、后台任务和审计日志中间件。
3. 注册统一异常处理器。
4. 把 API 挂载到 `/api/v1`。
5. 在 lifespan 启动阶段初始化数据库、管理员、菜单、API 和角色。
6. 服务关闭时释放 Tortoise 数据库连接。

### `app/api/v1/`

这里是 HTTP 路由层。`base` 负责登录和当前用户；`users`、`roles`、`menus`、`apis`、`depts`、`auditlog` 是系统管理模块；`courses`、`sessions`、`emoji`、`statistics`、`dashboard`、`ai` 是情绪课堂扩展点，目前部分接口仍是 TODO。

`app/api/v1/__init__.py` 负责组合子路由。管理端路由统一加 `DependPermission`，普通登录接口使用 `DependAuth`。新增模块完成前不要急于注册到总路由，避免空路由影响启动和 API 扫描。

### `app/models/`

数据持久化层使用 Tortoise ORM：

- `base.py` 提供自增主键、时间字段和模型序列化能力。
- `admin.py` 保存 User、Role、Menu、Api、Dept、AuditLog 等后台模型。
- `classroom.py` 是情绪课堂模型扩展位置，当前尚未完成 Course、ClassSession、ScheduleUser、EmojiRecord 等实体。
- `enums.py` 保存 ORM 使用的枚举，例如 API 请求方法。

模型变化后需要配套 Aerich 迁移，并同步检查初始化数据和权限数据。

### `app/schemas/`

Schema 是 Pydantic 请求/响应契约，不等同于数据库模型。接口参数先由 Schema 校验，再交给 Controller 或 Service 处理。情绪课堂需要补齐课程、课堂会话、排课用户、Emoji 类型和统计响应 Schema。

### `app/controllers/`

Controller 封装面向单个资源的查询和写入逻辑，并复用 `app/core/crud.py` 的分页、创建、更新、删除能力。课程、会话和 Emoji Controller 还需要补充教师/学生归属校验，不能只按 ID 查询后直接返回。

### `app/services/`

Service 用于跨接口或较复杂的业务：`statistics.py` 负责聚合 EmojiRecord，`export.py` 负责 CSV 导出和注入防护，`ai_ingest.py` 负责验证 AI 服务令牌、过滤低置信度结果并写入 EmojiRecord。

## 3. 前端目录

- `web/src/main.js`：创建 Vue 应用，安装 Store、Router、指令和 i18n。
- `web/src/router/`：基础路由、动态路由和登录守卫；登录后从后端获取菜单并转换为 Vue 路由。
- `web/src/store/`：Pinia 状态，重点是用户状态和权限菜单。
- `web/src/api/index.js`：集中定义后端接口调用，新增课程、会话、Emoji 和教师查询 API 时应按模块分组。
- `web/src/utils/http/`：Axios 实例、Token 注入、统一响应和错误处理。
- `web/src/views/`：页面级组件；系统管理页面已有基础实现，学生/教师情绪课堂页面需要新增。
- `web/src/components/`：表格、弹窗、查询栏、图标和页面容器等通用组件。

前端请求默认使用 `VITE_BASE_API`。请求拦截器会把登录 Token 放在 `token` 请求头，响应拦截器按照后端约定的 `code` 判断成功/失败，并在 401 时触发退出登录。

## 4. 四个成员模块的依赖

```text
A：模型、Schema、Controller、迁移、数据归属校验
├── B：学生/教师页面和 API 调用
├── C：管理端、统计、导出
└── D：AI 结果接入和 EmojiRecord 写入
```

- A 是数据契约和业务归属校验的基础，应先固定字段和接口示例。
- B 可以使用 Mock 数据并行开发页面，但联调依赖 A 的接口。
- C 依赖 A 的模型和查询字段，尤其是统计和导出。
- D 可以独立开发 AI 服务适配层，但必须提前约定 `session_id`、`source=AI`、`confidence` 和鉴权方式。

## 5. 一次请求的典型链路

```text
前端页面 → web/src/api/index.js → Axios 请求拦截器注入 token
→ /api/v1/{module}/{endpoint} → FastAPI Router
→ DependAuth / DependPermission → Schema 校验
→ Controller / Service → Tortoise Model
→ Success / Fail 响应 → Axios 响应拦截器
```

## 6. 开发和联调注意事项

1. 先完成模型、Schema、OpenAPI 示例和迁移，再让其他模块依赖真实字段。
2. 管理员接口使用 `DependPermission`；学生/教师接口除登录校验外，还必须校验资源归属。
3. AI 接口使用独立的 `AI_SERVICE_TOKEN`，不能把 AI 服务当成普通学生 JWT 客户端。
4. 修改模型后同步检查 `app/settings/config.py`、Aerich 迁移和初始化角色权限。
5. 新增后端路由时同步补充前端 API、接口测试、单元测试和 README 使用说明。
