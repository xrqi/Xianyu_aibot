# XianyuBot Docker 部署指南

## 🚀 快速启动（推荐）

### 方式1：使用启动脚本（交互式）

```bash
# 给脚本添加执行权限
chmod +x scripts/docker-start.sh

# 运行启动脚本
./scripts/docker-start.sh
```

脚本会自动：
1. 检查 `.env` 配置
2. 检查/导入 cookies
3. 验证 cookies 有效性
4. 启动 Docker 容器

### 方式2：手动启动（已有 cookies）

```bash
# 1. 确保 cookies 文件存在
ls -la data/xianyu_cookies.json

# 2. 直接启动
docker-compose up -d

# 3. 查看日志
docker-compose logs -f
```

---

## 📋 Cookies 导入方式

### 方式A：挂载本地文件（推荐）

```bash
# 将本地 cookies 放入 data 目录
cp /path/to/your/cookies.json data/xianyu_cookies.json

# 启动
docker-compose up -d
```

### 方式B：使用环境变量

```bash
# 将 cookies 内容设置为环境变量
export XIANYU_COOKIES='{"_m_h5_tk":"xxx","_m_h5_tk_enc":"xxx"}'

# 在 docker-compose.yml 中添加环境变量，然后启动
docker-compose up -d
```

### 方式C：启动后进入容器登录

```bash
# 1. 先启动容器（会报错缺少 cookies，没关系）
docker-compose up -d

# 2. 进入容器
docker-compose exec xianyubot bash

# 3. 在容器内执行登录
python run.py --manual-cookies '你的cookies字符串'

# 4. 退出容器，cookies 已保存
docker-compose restart
```

### 方式D：复制本地 cookies 到运行中的容器

```bash
# 如果容器已在运行，复制 cookies 进去
docker cp data/xianyu_cookies.json xianyubot:/app/data/

# 重启容器
docker-compose restart
```

---

## 🔧 常用命令

```bash
# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 进入容器
docker-compose exec xianyubot bash

# 重新构建
docker-compose up -d --build

# 查看 Web 反馈后台
open http://localhost:5000
```

---

## ⚠️ 常见问题

### 1. 提示缺少 cookies

```
❌ 无法启动：缺少 cookies
```

**解决**: 使用上述任意一种方式导入 cookies

### 2. cookies 过期

```
FAIL_SYS_USER_VALIDATE
```

**解决**: 
```bash
# 1. 进入容器
docker-compose exec xianyubot bash

# 2. 更新 cookies
python run.py --manual-cookies '新的cookies'

# 3. 重启
docker-compose restart
```

### 3. 端口被占用

```
Bind for 0.0.0.0:5000 failed: port is already allocated
```

**解决**: 修改 `docker-compose.yml` 中的端口映射
```yaml
ports:
  - "5001:5000"  # 改为 5001 或其他端口
```

### 4. 时区问题

容器默认使用 `Asia/Shanghai` 时区，如需修改：

```yaml
environment:
  - TZ=Asia/Shanghai  # 改为你的时区
```

---

## 🌐 访问服务

| 服务 | 地址 | 说明 |
|-----|------|------|
| Web 反馈后台 | http://服务器IP:5000 | 标记对话、查看统计 |
| Nginx (如启用) | http://服务器IP | 反向代理 |

---

## 💾 数据持久化

以下数据会持久化保存：

| 路径 | 说明 |
|-----|------|
| `./data/chat_history.db` | 对话历史数据库 |
| `./data/xianyu_cookies.json` | 登录凭证 |
| `./data/*.bak` | 自动备份文件 |

删除容器不会丢失这些数据。

---

## 🔒 安全建议

1. **不要在 Dockerfile 中硬编码 cookies**
2. **使用 .env 文件管理敏感信息**（已加入 .gitignore）
3. **生产环境启用 HTTPS**（配置 nginx/ssl/ 目录）
4. **限制端口访问**（使用防火墙）

```bash
# 仅允许特定 IP 访问 5000 端口
ufw allow from 你的IP to any port 5000
```
