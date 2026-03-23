# XianyuBot 系统架构文档

## 1. 系统概述

XianyuBot 是一个基于大语言模型的闲鱼智能客服机器人，实现7×24小时自动化值守，支持多专家协同决策、智能议价和上下文感知对话。

### 1.1 核心特性
- 🤖 **AI驱动**：基于通义千问等大模型生成自然回复
- 🧠 **持续学习**：记录对话效果，自动优化回复策略
- 💰 **智能议价**：根据议价次数动态调整价格策略
- 📊 **数据分析**：追踪成交率、用户偏好等关键指标
- 🔒 **安全可靠**：内置内容安全过滤，遵守平台规则

## 2. 系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户交互层                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  闲鱼买家   │  │  WebSocket  │  │   反馈收集工具      │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
└─────────┼────────────────┼────────────────────┼────────────┘
          │                │                    │
          ▼                ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                        业务逻辑层                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              XianyuLive (WebSocket处理)               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │  │  消息接收   │  │  消息解析   │  │  回复发送    │  │  │
│  │  └─────────────┘  └─────────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           XianyuReplyBot (回复生成引擎)               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │  │ 意图识别   │  │ 策略选择   │  │ 回复生成    │  │  │
│  │  └─────────────┘  └─────────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              LearningEngine (学习引擎)                │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │  │ 效果追踪   │  │ 偏好学习   │  │ 策略优化    │  │  │
│  │  └─────────────┘  └─────────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                        数据存储层                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  SQLite DB  │  │  Cookies    │  │    配置文件         │ │
│  │  (对话历史) │  │  (登录凭证) │  │   (.env, prompts)   │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                        外部服务层                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  通义千问   │  │  闲鱼API    │  │   WebSocket服务     │ │
│  │  (LLM)      │  │  (消息接口) │  │   (实时通信)        │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 模块说明

#### 2.2.1 API层 (`src/api/`)

| 模块 | 功能 | 关键类/函数 |
|-----|------|-----------|
| `xianyu_websocket.py` | WebSocket连接管理 | `XianyuWebSocket`, `XianyuLive` |
| `xianyu_api.py` | 闲鱼REST API调用 | `XianyuAPI` |

**XianyuLive 核心功能：**
- 建立并维护WebSocket连接
- 接收和解析闲鱼消息
- 消息去重和过滤
- 调用AI生成回复
- 发送回复消息

#### 2.2.2 Agent层 (`src/agents/`)

| 模块 | 功能 | 关键类 |
|-----|------|-------|
| `base.py` | Agent基类 | `BaseAgent` |
| `expert_agents.py` | 专家Agent实现 | `PriceAgent`, `TechAgent`, `XianyuReplyBot` |

**XianyuReplyBot 核心功能：**
- 意图识别（价格/技术/默认）
- 动态提示词构建
- 调用大模型生成回复
- 安全过滤
- 学习偏好应用

#### 2.2.3 Core层 (`src/core/`)

| 模块 | 功能 | 关键类 |
|-----|------|-------|
| `context_manager.py` | 对话上下文管理 | `ChatContextManager` |
| `learning_engine.py` | AI学习引擎 | `LearningEngine` |

**ChatContextManager：**
- SQLite数据库存储
- 对话历史管理
- 议价次数追踪
- 用户统计信息

**LearningEngine：**
- 对话结果记录
- 回复效果评估
- 用户偏好学习
- 策略效果分析
- 生成学习报告

#### 2.2.4 Utils层 (`src/utils/`)

| 模块 | 功能 |
|-----|------|
| `xianyu_apis.py` | 闲鱼API封装（token获取、商品信息） |
| `xianyu_utils.py` | 工具函数（cookies管理、加密解密） |

## 3. 数据流

### 3.1 消息处理流程

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 接收消息 │───▶│ 消息解析 │───▶│ 意图识别 │───▶│ 生成回复 │
└──────────┘    └──────────┘    └──────────┘    └────┬─────┘
                                                     │
┌──────────┐    ┌──────────┐    ┌──────────┐        │
│ 发送回复 │◀───│ 安全过滤 │◀───│ LLM调用  │◀───────┘
└──────────┘    └──────────┘    └──────────┘
```

### 3.2 学习流程

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 记录回复 │───▶│ 追踪反馈 │───▶│ 分析效果 │───▶│ 优化策略 │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

## 4. 数据模型

### 4.1 数据库表结构

#### messages（消息表）
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,      -- 用户ID
    item_id TEXT NOT NULL,      -- 商品ID
    role TEXT NOT NULL,         -- 角色(user/assistant)
    content TEXT NOT NULL,      -- 消息内容
    timestamp DATETIME          -- 时间戳
);
```

#### bargain_counts（议价次数表）
```sql
CREATE TABLE bargain_counts (
    user_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    count INTEGER DEFAULT 0,    -- 议价次数
    last_updated DATETIME
);
```

#### conversation_outcomes（对话结果表）
```sql
CREATE TABLE conversation_outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    outcome TEXT,               -- deal/no_deal/ongoing
    final_price REAL,           -- 成交价
    original_price REAL,        -- 原价
    message_count INTEGER       -- 消息数量
);
```

#### reply_effectiveness（回复效果表）
```sql
CREATE TABLE reply_effectiveness (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    reply_type TEXT,            -- price/tech/default
    reply_content TEXT,
    user_response TEXT,
    is_positive BOOLEAN         -- 是否积极回应
);
```

#### user_preferences（用户偏好表）
```sql
CREATE TABLE user_preferences (
    user_id TEXT PRIMARY KEY,
    price_sensitivity TEXT,     -- high/medium/low
    successful_strategies TEXT, -- JSON
    last_updated DATETIME
);
```

## 5. 配置说明

### 5.1 环境变量 (.env)

```bash
# API配置
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 模型配置
LLM_MODEL=qwen3-flash        # 主模型
LLM_MODEL_LIGHT=qwen3-flash  # 轻量模型
LLM_TEMPERATURE=0.7          # 温度参数

# 日志配置
LOG_LEVEL=INFO
DEBUG=False
```

### 5.2 提示词配置 (prompts/unified_prompt.txt)

系统提示词定义了AI的行为准则，包括：
- 角色定位
- 情绪感知能力
- 商品理解能力
- 议价策略
- 安全规则

## 6. 安全机制

### 6.1 内容安全过滤
- 自动过滤联系方式（微信、QQ、电话）
- 禁止线下交易提议
- 敏感词检测

### 6.2 数据安全
- Cookies本地加密存储
- 数据库访问隔离
- 无敏感信息日志记录

## 7. 扩展性设计

### 7.1 添加新的专家Agent
```python
class NewAgent(BaseAgent):
    def generate(self, user_msg, item_desc, context, bargain_count=0):
        # 实现特定逻辑
        pass
```

### 7.2 自定义学习策略
在 `LearningEngine` 中添加新的分析方法：
```python
def analyze_new_pattern(self):
    # 实现新的分析逻辑
    pass
```

## 8. 性能优化

### 8.1 并发处理
- WebSocket消息异步处理
- LLM调用线程池管理
- 数据库连接池

### 8.2 缓存机制
- 消息指纹去重
- 用户偏好缓存
- 系统通知去重

## 9. 监控与日志

### 9.1 日志级别
- `DEBUG`: 详细调试信息
- `INFO`: 正常运行信息
- `WARNING`: 警告信息
- `ERROR`: 错误信息

### 9.2 关键指标
- 消息响应时间
- 对话成交率
- 用户满意度
- 系统稳定性

## 10. 部署架构

### 10.1 单机部署
```
[用户] <--WebSocket--> [XianyuBot] <--API--> [通义千问]
                           │
                           ▼
                      [SQLite DB]
```

### 10.2 推荐配置
- CPU: 2核+
- 内存: 4GB+
- 磁盘: 10GB+
- 网络: 稳定互联网连接
