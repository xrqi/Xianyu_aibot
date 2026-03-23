<p align="right">
   <strong>中文</strong> | <a href="./README.en.md">English</a>
</p>

<div align="center">

# 🚀 XianyuBot

<img src="./assets/logo.png" alt="XianyuBot Logo" width="180">

模块化闲鱼客服机器人系统，实现闲鱼平台7×24小时自动化值守，支持多专家协同决策、智能议价、上下文感知对话和AI持续学习进化。

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python Version">
  </a>
  <a href="https://platform.openai.com/">
    <img src="https://img.shields.io/badge/LLM-powered-FF6F61" alt="LLM Powered">
  </a>
  <a href="https://raw.githubusercontent.com/yourusername/xianyubot/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-brightgreen" alt="license">
  </a>
</p>

</div>

## 📝 项目说明

> [!NOTE]  
> XianyuBot 是基于 [XianyuAutoAgent](https://github.com/shaxiu/XianyuAutoAgent) 重构的模块化闲鱼智能客服系统，提供了更完善的架构和更强大的功能。

> [!IMPORTANT]  
> - 本项目仅供个人学习使用，不保证稳定性，请勿用于商业用途。
> - 使用者必须在遵循闲鱼平台规则以及相关法律法规的情况下使用，不得用于非法用途。

## ✨ 核心特性

<table>
<tr>
<th>模块化架构</th>
<th>智能对话引擎</th>
<th>AI持续进化</th>
</tr>
<tr>
<td>

- 🧩 **核心模块分离** - 聊天上下文、Agent决策、API接口完全解耦
- 🔌 **插件式设计** - 支持自定义专家插件开发
- 🛠️ **配置灵活** - 独立配置文件管理
- 🐳 **Docker支持** - 一键部署，轻松运维

</td>
<td>

- 💬 **上下文感知** - 完整对话历史记忆管理
- 🧠 **专家路由** - 基于意图识别的多专家动态分发
- 💰 **议价系统** - 智能阶梯降价策略
- 😊 **情绪感知** - 识别买家情绪并调整回复策略

</td>
<td>

- 📊 **效果追踪** - 自动记录每次对话结果
- 🎯 **偏好学习** - 学习用户价格敏感度和回复偏好
- 🔄 **策略优化** - 根据成交数据优化回复策略
- 🌐 **Web反馈后台** - 可视化标记对话和查看统计

</td>
</tr>
</table>

## 🚴 快速开始

### 环境要求
- Python 3.8+
- Playwright (获取登录凭证)

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/xianyubot.git
cd xianyubot

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装Playwright浏览器
python -m playwright install firefox chromium

# 4. 配置环境变量
cp .env.example .env
# 编辑.env文件，填入必要的API密钥和配置
```

### 大模型配置

XianyuBot支持通过环境变量配置不同的大模型，您可以在`.env`文件中设置以下参数：

```bash
# 主要模型 - 用于生成回复（推荐通义千问）
LLM_MODEL=qwen3-flash

# 轻量级模型 - 用于分类等简单任务
LLM_MODEL_LIGHT=qwen3-flash

# 温度参数 - 控制回复的创意性 (0.0-2.0)
LLM_TEMPERATURE=0.7
```

推荐的模型：
- **通义千问**（推荐）：`qwen3-flash`（极速）、`qwen-max`（最强）、`qwen-plus`（平衡）
- OpenAI API模型：`gpt-4o`、`gpt-4o-mini`等
- 其他兼容OpenAI API格式的模型：`glm-4`、`deepseek`等

获取通义千问API密钥：[阿里云百炼](https://bailian.console.aliyun.com/)

## 💻 使用方法

### 获取登录凭证

XianyuBot支持多种方式获取登录凭证：

<table>
<tr>
<th>方式一：手动导入Cookies（推荐）</th>
<th>方式二：使用命令行参数登录</th>
</tr>
<tr>
<td>

```bash
# 1. 浏览器登录闲鱼，复制cookies
# 2. 保存到 data/xianyu_cookies.json
# 3. 直接启动
python start_bot.py
```

</td>
<td>

```bash
# 使用--manual-cookies参数直接传入
python run.py --manual-cookies '你的cookies字符串'
```

</td>
</tr>
</table>

> **注意**：扫码登录无法使用WebSocket，必须使用账号密码登录获取 `unb` 或 `havana_lgc2_77` 字段的cookies。

### 运行主程序

```bash
# 方式1：使用简化启动脚本（推荐）
python start_bot.py

# 方式2：使用原始启动方式
python run.py

# 方式3：Docker部署
docker-compose up -d
```

### 命令行参数

| 参数 | 说明 |
|------|------|
| `--manual-cookies` | 手动传入cookies字符串，格式为JSON |
| `--debug` | 启用调试模式，输出更详细的日志信息 |

示例：
```bash
# 使用手动cookies启动
python run.py --manual-cookies '{"_m_h5_tk":"xxx","_m_h5_tk_enc":"xxx","unb":"xxx"}'

# 启用调试模式
python run.py --debug
```

## 🖥️ 系统兼容性

XianyuBot 目前支持以下操作系统：

<table>
<tr>
<th>macOS支持</th>
<th>Windows支持</th>
</tr>
<tr>
<td>

- 使用Firefox浏览器获取登录凭证
- 自动处理路径和权限
- 完全支持所有功能

</td>
<td>

- 使用`Chromium`浏览器代替Firefox获取登录凭证
- 优化路径处理，解决目录分隔符问题
- 解决`asyncio`事件循环兼容性问题

</td>
</tr>
</table>

## 📁 项目结构

```
xianyubot/
├── data/                      # 数据存储目录
│   ├── chat_history.db        # SQLite数据库（对话历史）
│   └── xianyu_cookies.json    # 登录凭证
├── src/                       # 源代码目录
│   ├── api/                   # API接口模块
│   │   ├── xianyu_api.py
│   │   └── xianyu_websocket.py
│   ├── agents/                # 智能代理模块
│   │   ├── base.py
│   │   └── expert_agents.py
│   ├── core/                  # 核心功能模块
│   │   ├── context_manager.py
│   │   └── learning_engine.py # AI学习引擎
│   └── utils/                 # 工具函数
├── web/                       # Web反馈后台
│   ├── feedback_server.py
│   └── templates/
├── prompts/                   # 提示词模板
│   └── unified_prompt.txt
├── scripts/                   # 辅助脚本
│   ├── docker-start.sh        # Docker启动脚本
│   └── docker-entrypoint.sh   # Docker入口脚本
├── docs/                      # 文档
│   ├── architecture.md        # 系统架构文档
│   └── usage.md               # 使用文档
├── docker-compose.yml         # Docker Compose配置
├── Dockerfile                 # Docker镜像配置
├── start_bot.py               # 简化启动脚本
├── feedback.py                # 命令行反馈工具
├── run.py                     # 主程序入口
├── requirements.txt           # 依赖列表
├── .env.example               # 环境变量示例
└── README.md                  # 项目文档
```

## 🧩 系统架构

XianyuBot 采用模块化分层架构设计：

<table>
<tr>
<th>层级</th>
<th>功能</th>
</tr>
<tr>
<td><strong>API层</strong></td>
<td>

- 实现WebSocket连接维护
- 消息收发管理
- 会话状态监控

</td>
</tr>
<tr>
<td><strong>核心层</strong></td>
<td>

- 上下文管理：记忆对话历史
- 状态追踪：跟踪交易阶段
- 消息路由：分发到合适的专家代理

</td>
</tr>
<tr>
<td><strong>代理层</strong></td>
<td>

- 基础代理：提供通用对话能力
- 专家代理：处理特定场景（议价、物流等）
- 协同机制：多专家协作决策

</td>
</tr>
<tr>
<td><strong>工具层</strong></td>
<td>

- 登录管理：自动获取和刷新登录凭证
- 配置管理：灵活的环境变量控制

</td>
</tr>
</table>

## 📊 性能与限制

| 指标 | 数值/说明 |
|------|-----------|
| **响应速度** | 平均回复时间 < 3秒 |
| **并发处理** | 单实例支持多会话并发 |
| **内存占用** | 约150-300MB（取决于活跃会话数量） |
| **API额度** | 取决于您的OpenAI API Key限制 |

## 🐳 Docker部署

### 快速启动

```bash
# 1. 准备cookies文件
cp your_cookies.json data/xianyu_cookies.json

# 2. 使用启动脚本（交互式）
chmod +x scripts/docker-start.sh
./scripts/docker-start.sh

# 或手动启动
docker-compose up -d
```

### 访问服务

- **Web反馈后台**: http://localhost:5000
- **查看日志**: `docker-compose logs -f`

详细部署指南：[DOCKER_DEPLOY.md](./DOCKER_DEPLOY.md)

---

## 🧠 AI训练与优化

### Web反馈后台

启动Web服务器后，可以可视化地标记对话结果：

```bash
# 启动Web反馈后台
cd web && python feedback_server.py

# 或Docker方式
docker-compose up -d
```

功能：
- 📊 查看对话统计报告
- 💬 浏览历史对话记录
- 🏷️ 标记对话结果（成交/未成交/进行中）
- 📈 查看AI学习效果

### 命令行反馈工具

```bash
# 查看统计
python feedback.py stats

# 标记对话结果
python feedback.py record <用户ID> <商品ID> deal <成交价> <原价>
```

> **提示**: 定期标记对话结果（建议每天5-10个），帮助AI更快学习和优化回复策略。

---

## 🔮 未来计划

- [x] Web管理界面（可视化配置和监控）✅
- [x] AI持续学习系统（反馈优化）✅
- [x] Docker一键部署 ✅
- [ ] 知识库管理（支持RAG增强回复质量）
- [ ] 兼容各种模型后端（欢迎提交issues建议）
- [ ] 添加更多专家代理类型
- [ ] 支持多账号同时在线
- [ ] 移动端管理App

## 🤝 贡献与支持

欢迎提交Issue和Pull Request，共同改进XianyuBot！如有使用问题，请在GitHub上提交详细的错误报告。

## 📄 许可证

本项目采用MIT许可证开源。

## 🧸 特别鸣谢

本项目基于以下开源项目重构：
- [XianyuAutoAgent](https://github.com/shaxiu/XianyuAutoAgent) - 智能闲鱼客服机器人系统，由 [@shaxiu](https://github.com/shaxiu) 和 [@cv-cat](https://github.com/cv-cat) 开发