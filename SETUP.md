# 运行说明

仓库首页是带截图的项目介绍。下面是本机启动步骤。

管理员后台：维护分类、图书、读者，办理借书和还书。

- 前端：Vue2 + Element UI
- 后端：Django 4.2 + Django REST Framework
- 登录：JWT
- 数据库：MySQL

业务表四张：分类、图书、读者、借还记录。
借书时检查剩余量和读者可借数量，通过后剩余减 1 并写记录；还书后剩余加 1。应还日期为借出当天加 30 天。

---

## 1. 环境准备

- Python 3
- Node.js
- MySQL（已启动）

---

## 2. 数据库

### 2.1 建库

库名：`book_borrow_management_system`  
字符集：`utf8mb4`

### 2.2 改配置

在 `backend/backend/settings.py`里改数据库账号和密码等

---

## 3. 启动后端

进入后端目录：

```bash
cd backend
```

第一次需要创建虚拟环境（已有 `backend/venv` 则跳过这一步）：

```bash
python -m venv venv
```

Windows PowerShell 激活虚拟环境：

```bash
.\venv\Scripts\Activate.ps1
```

提示符前面出现 `(venv)` 后再安装依赖、建表、创建管理员：

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`createsuperuser` 时按提示输入用户名和密码。本仓库演示账号名为 `admin1`

后端地址：`http://127.0.0.1:8000/`

接口前缀：`/api/`。不要只打开根地址，没有首页，出现 404 是正常的。

已经建过环境、装过依赖的，下次只要：

```bash
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

---

## 4. 启动前端

另开一个终端，进入前端目录：

```bash
cd frontend
npm install
npm run dev
```

已经装过依赖的，下次只要：

```bash
cd frontend
npm run dev
```

浏览器打开：`http://localhost:9528`

开发时代理：前端请求 `/dev-api`，转发到后端 `http://127.0.0.1:8000/api`。

登录后默认进入图书分类页。Access Token 有效期 2 小时，过期后重新登录即可，数据不会丢。

---

## 5. 目录说明

```text
图书借阅管理系统/
  backend/                 Django 项目
    apps/library/          分类、图书、读者、借还
    apps/users/            登录、当前用户信息
    backend/settings.py    数据库、JWT、跨域
  frontend/                Vue 后台
    src/views/library/     四个业务页面
    src/api/library.js     对应接口
    src/router/index.js    菜单路由
```

---

## 6. 主要接口

| 说明     | 方法 | 地址 |
| -------- | ---- | ---- |
| 登录     | POST | `/api/login/` |
| 当前用户 | GET  | `/api/user/info/` |
| 分类     | CRUD | `/api/book-categories/` |
| 图书     | CRUD | `/api/books/` |
| 读者     | CRUD | `/api/readers/` |
| 借还记录 | CRUD | `/api/borrows/` |
| 还书     | POST | `/api/borrows/{id}/return/` |

登录成功后，请求头带：`Authorization: Bearer <token>`。
