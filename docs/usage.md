# XianyuBot 使用文档

## 目录
1. [快速开始](#快速开始)
2. [配置说明](#配置说明)
3. [日常使用](#日常使用)
4. [AI训练与优化](#ai训练与优化)
5. [故障排除](#故障排除)
6. [高级功能](#高级功能)

---

## 快速开始

### 1. 环境要求
- Python 3.8+
- Windows/macOS/Linux
- 稳定的网络连接

### 2. 安装步骤

```bash
# 1. 进入项目目录
cd xianyu_ai_bot

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装Playwright浏览器
python -m playwright install chromium
```

### 3. 配置API密钥

编辑 `.env` 文件：

```bash
# 通义千问API（推荐）
OPENAI_API_KEY=sk-your-api-key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 模型选择
LLM_MODEL=qwen3-flash        # 极速模型，响应快
# LLM_MODEL=qwen-max         # 最强模型，质量高
# LLM_MODEL=qwen-plus        # 平衡选择
```

> 💡 **获取API密钥**：访问 [阿里云百炼](https://bailian.console.aliyun.com/) 创建API密钥

### 4. 首次启动

#### 方式一：手动输入Cookies（推荐）

1. **获取Cookies**：
   - 浏览器访问 https://www.goofish.com
   - 账号密码登录（完成滑动验证）
   - 按 F12 → Network → 刷新页面
   - 点击任意请求，复制Cookies

2. **启动机器人**：
   ```bash
   python run.py --manual-cookies "你的cookies字符串"
   ```

#### 方式二：浏览器自动登录

```bash
python run.py --login
```

> ⚠️ 此方式会打开浏览器窗口，需要手动完成登录和滑动验证

---

## 配置说明

### 环境变量配置 (.env)

| 变量名 | 说明 | 默认值 | 可选值 |
|-------|------|--------|--------|
| `OPENAI_API_KEY` | API密钥 | - | 你的密钥 |
| `OPENAI_BASE_URL` | API基础URL | - | 阿里云/其他 |
| `LLM_MODEL` | 主模型 | qwen-max | qwen3-flash, qwen-plus |
| `LLM_MODEL_LIGHT` | 轻量模型 | qwen-turbo | qwen3-flash |
| `LLM_TEMPERATURE` | 创意度 | 0.7 | 0.0-2.0 |
| `LOG_LEVEL` | 日志级别 | INFO | DEBUG, WARNING, ERROR |
| `DEBUG` | 调试模式 | False | True, False |

### 模型选择建议

| 场景 | 推荐模型 | 说明 |
|-----|---------|------|
| 追求速度 | `qwen3-flash` | 响应最快，适合客服场景 |
| 追求质量 | `qwen-max` | 回复质量最高 |
| 平衡选择 | `qwen-plus` | 速度和质量兼顾 |

---

## 日常使用

### 启动机器人

```bash
# 方式1：使用 run.py（推荐）
python run.py

# 方式2：使用简化启动脚本
python start_bot.py
```

> 💡 首次之后，程序会自动加载保存的cookies，无需重复输入

### 查看运行日志

启动后，终端会显示实时日志：

```
2026-03-23 18:00:00 | INFO | 成功加载登录凭证
2026-03-23 18:00:01 | INFO | WebSocket连接已建立
2026-03-23 18:00:05 | INFO | 收到用户 xxx 的消息: 能不能便宜点
2026-03-23 18:00:06 | INFO | 机器人回复: 您好！感谢您的关注...
```

### 停止机器人

按 `Ctrl + C` 即可安全停止

---

## AI训练与优化

### 1. 标记对话结果（重要）

帮助AI学习，提高回复质量：

```bash
# 查看最近对话
python feedback.py list

# 交互式标记
python feedback.py list --feedback

# 命令行直接标记
python feedback.py record <用户ID> <商品ID> <结果> [成交价] [原价]
```

**结果类型**：
- `deal` - 成交
- `no_deal` - 未成交
- `ongoing` - 进行中

**示例**：
```bash
python feedback.py record 123456 item789 deal 80 100
```

### 2. 查看学习报告

```bash
python feedback.py stats
```

输出示例：
```
📊 本周学习报告
总对话数: 50
成交数: 15
转化率: 30.0%
平均折扣: 12.5%
```

### 3. AI如何进化

#### 短期适应（单对话内）
- ✅ 记住用户议价次数
- ✅ 根据次数调整策略
- ✅ 保持对话上下文

#### 长期学习（多对话间）
- ✅ 分析哪种回复导致成交
- ✅ 学习用户价格敏感度
- ✅ 积累商品最佳卖点
- ✅ 优化回复策略

### 4. 优化建议

1. **定期标记结果**：每天至少标记5-10个对话结果
2. **观察学习报告**：了解转化率和用户偏好
3. **调整提示词**：根据业务需求修改 `prompts/unified_prompt.txt`
4. **选择合适的模型**：根据响应速度需求选择模型

---

## 故障排除

### 常见问题

#### 1. Cookies过期

**症状**：
```
❌ Cookies 已过期或需要验证
```

**解决**：
```bash
# 重新获取cookies
python run.py --manual-cookies "新的cookies"
```

#### 2. API调用失败

**症状**：
```
ERROR | 模型调用失败
```

**检查**：
- API密钥是否正确
- 账户余额是否充足
- 网络连接是否正常

#### 3. WebSocket连接断开

**症状**：
```
WebSocket连接已关闭，将尝试重新连接
```

**说明**：这是正常现象，程序会自动重连。如果频繁断开，检查网络稳定性。

#### 4. 回复质量下降

**可能原因**：
- 模型切换到了轻量版
- 温度参数设置过高
- 提示词需要优化

**解决**：
```bash
# 检查当前模型
python -c "import os; print(os.getenv('LLM_MODEL'))"

# 修改 .env 使用更强的模型
LLM_MODEL=qwen-max
```

### 日志分析

日志文件位置：`data/chat_history.db`（SQLite数据库）

查看最近错误：
```bash
# 实时查看日志
python run.py 2>&1 | grep ERROR
```

---

## 高级功能

### 1. 自定义提示词

编辑 `prompts/unified_prompt.txt`：

```
你是闲鱼平台上一位经验丰富的卖家...

## 核心能力
1. **情绪感知与回应**
   - 识别买家情绪...
   
2. **商品信息深度理解**
   - 基于商品标题和描述...
```

### 2. 数据库查询

```bash
# 进入SQLite命令行
sqlite3 data/chat_history.db

# 查看最近消息
SELECT * FROM messages ORDER BY timestamp DESC LIMIT 10;

# 查看用户统计
SELECT user_id, COUNT(*) FROM messages GROUP BY user_id;

# 查看议价次数
SELECT * FROM bargain_counts ORDER BY count DESC;
```

### 3. 备份数据

```bash
# 备份数据库
cp data/chat_history.db data/chat_history_$(date +%Y%m%d).bak

# 备份cookies
cp data/xianyu_cookies.json data/xianyu_cookies_$(date +%Y%m%d).bak
```

### 4. 批量导入历史数据

如需导入历史对话数据，直接操作SQLite数据库：

```python
import sqlite3

conn = sqlite3.connect('data/chat_history.db')
cursor = conn.cursor()

# 插入历史数据
cursor.execute('''
    INSERT INTO messages (user_id, item_id, role, content, timestamp)
    VALUES (?, ?, ?, ?, ?)
''', ('user123', 'item456', 'user', '历史消息', '2026-03-23 10:00:00'))

conn.commit()
conn.close()
```

---

## 最佳实践

### 1. 日常维护
- ✅ 每天检查一次日志，确认运行正常
- ✅ 每周标记至少20个对话结果
- ✅ 每月查看学习报告，分析转化率
- ✅ 定期备份数据库和cookies

### 2. 性能优化
- ✅ 使用 `qwen3-flash` 模型保证响应速度
- ✅ 适当调整 `LLM_TEMPERATURE`（0.6-0.8）
- ✅ 定期清理旧数据（保留30天）

### 3. 安全建议
- ✅ 不要分享 `.env` 文件
- ✅ 定期更换API密钥
- ✅ cookies过期后立即删除旧文件
- ✅ 不要在公共网络运行

---

## 更新日志

### v1.0.0 (2026-03-23)
- ✅ 基础对话功能
- ✅ 智能议价系统
- ✅ 学习引擎
- ✅ 反馈收集工具
- ✅ 自动cookies管理

---

## 获取帮助

如有问题：
1. 查看日志文件
2. 检查 `.env` 配置
3. 确认cookies有效性
4. 查看架构文档了解系统原理

---

**提示**：本文档与代码同步更新，建议定期查看是否有新版本。
