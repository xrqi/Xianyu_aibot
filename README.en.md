<p align="right">
   <a href="./README.md">中文</a> | <strong>English</strong>
</p>

<div align="center">

# 🚀 XianyuBot

<img src="./assets/logo.png" alt="XianyuBot Logo" width="180">

A modular Xianyu customer service bot system, providing 24/7 automated support on the Xianyu platform, featuring multi-expert collaborative decision-making, intelligent price negotiation, context-aware conversations, and continuous AI learning.

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

## 📝 Project Description

> [!NOTE]  
> XianyuBot is a modular Xianyu intelligent customer service system rebuilt based on [XianyuAutoAgent](https://github.com/shaxiu/XianyuAutoAgent), providing a more comprehensive architecture and more powerful features.

> [!IMPORTANT]  
> - This project is for personal learning purposes only, stability is not guaranteed, and it should not be used for commercial purposes.
> - Users must comply with Xianyu platform rules and relevant laws and regulations, and must not use it for illegal purposes.

## ✨ Core Features

<table>
<tr>
<th>Modular Architecture</th>
<th>Intelligent Conversation Engine</th>
<th>Continuous AI Evolution</th>
</tr>
<tr>
<td>

- 🧩 **Core Module Separation** - Chat context, Agent decision-making, and API interfaces completely decoupled
- 🔌 **Plugin Design** - Support for custom expert plugin development
- 🛠️ **Flexible Configuration** - Independent configuration file management
- 🐳 **Docker Support** - One-click deployment, easy operation

</td>
<td>

- 💬 **Context Awareness** - Complete dialogue history memory management
- 🧠 **Expert Routing** - Intent-based dynamic dispatch to multiple experts
- 💰 **Negotiation System** - Intelligent tiered price reduction strategy
- 😊 **Emotion Recognition** - Detect buyer emotions and adjust responses

</td>
<td>

- 📊 **Performance Tracking** - Automatically record conversation outcomes
- 🎯 **Preference Learning** - Learn user price sensitivity and response preferences
- 🔄 **Strategy Optimization** - Optimize reply strategies based on transaction data
- 🌐 **Web Feedback Dashboard** - Visual conversation marking and statistics

</td>
</tr>
</table>

## 🚴 Quick Start

### Requirements
- Python 3.8+
- Playwright (for obtaining login credentials)

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/xianyubot.git
cd xianyubot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
python -m playwright install firefox chromium

# 4. Configure environment variables
cp .env.example .env
# Edit the .env file and fill in the necessary API keys and configurations
```

### Large Language Model Configuration

XianyuBot supports configuration of different large language models through environment variables. You can set the following parameters in the `.env` file:

```bash
# Main model - used for generating responses (Tongyi Qianwen recommended)
LLM_MODEL=qwen3-flash

# Lightweight model - used for classification and other simple tasks
LLM_MODEL_LIGHT=qwen3-flash

# Temperature parameter - controls the creativity of responses (0.0-2.0)
LLM_TEMPERATURE=0.7
```

Recommended models:
- **Tongyi Qianwen** (Recommended): `qwen3-flash` (fastest), `qwen-max` (most powerful), `qwen-plus` (balanced)
- OpenAI API models: `gpt-4o`, `gpt-4o-mini`, etc.
- Other OpenAI API compatible models: `glm-4`, `deepseek`, etc.

Get Tongyi Qianwen API Key: [Alibaba Cloud Bailian](https://bailian.console.aliyun.com/)

## 💻 Usage Instructions

### Obtaining Login Credentials

XianyuBot supports multiple ways to obtain login credentials:

<table>
<tr>
<th>Method 1: Manual Cookie Import (Recommended)</th>
<th>Method 2: Using Command Line Parameters</th>
</tr>
<tr>
<td>

```bash
# 1. Login to Xianyu in browser and copy cookies
# 2. Save to data/xianyu_cookies.json
# 3. Start directly
python start_bot.py
```

</td>
<td>

```bash
# Use --manual-cookies parameter to pass cookies directly
python run.py --manual-cookies 'your_cookies_string'
```

</td>
</tr>
</table>

> **Note**: QR code login cannot use WebSocket. You must use account/password login to obtain cookies with `unb` or `havana_lgc2_77` fields.

### Running the Main Program

```bash
# Method 1: Using simplified startup script (Recommended)
python start_bot.py

# Method 2: Using original startup method
python run.py

# Method 3: Docker deployment
docker-compose up -d
```

### Command Line Arguments

| Parameter | Description |
|------|------|
| `--manual-cookies` | Manually pass cookies string in JSON format |
| `--debug` | Enable debug mode, outputting more detailed log information |

Example:
```bash
# Start with manual cookies
python run.py --manual-cookies '{"_m_h5_tk":"xxx","_m_h5_tk_enc":"xxx","unb":"xxx"}'

# Enable debug mode
python run.py --debug
```

## 🖥️ System Compatibility

XianyuBot currently supports the following operating systems:

<table>
<tr>
<th>macOS Support</th>
<th>Windows Support</th>
</tr>
<tr>
<td>

- Uses Firefox browser to obtain login credentials
- Automatically handles paths and permissions
- Full support for all features

</td>
<td>

- Uses `Chromium` browser instead of Firefox to obtain login credentials
- Optimized path handling, resolving directory separator issues
- Resolves `asyncio` event loop compatibility issues

</td>
</tr>
</table>

## 📁 Project Structure

```
xianyubot/
├── data/                      # Data storage directory
│   ├── chat_history.db        # SQLite database (conversation history)
│   └── xianyu_cookies.json    # Login credentials
├── src/                       # Source code directory
│   ├── api/                   # API interface module
│   │   ├── xianyu_api.py
│   │   └── xianyu_websocket.py
│   ├── agents/                # Intelligent agent module
│   │   ├── base.py
│   │   └── expert_agents.py
│   ├── core/                  # Core functionality module
│   │   ├── context_manager.py
│   │   └── learning_engine.py # AI learning engine
│   └── utils/                 # Utility functions
├── web/                       # Web feedback dashboard
│   ├── feedback_server.py
│   └── templates/
├── prompts/                   # Prompt templates
│   └── unified_prompt.txt
├── scripts/                   # Helper scripts
│   ├── docker-start.sh        # Docker startup script
│   └── docker-entrypoint.sh   # Docker entrypoint script
├── docs/                      # Documentation
│   ├── architecture.md        # System architecture document
│   └── usage.md               # Usage document
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker image configuration
├── start_bot.py               # Simplified startup script
├── feedback.py                # Command line feedback tool
├── run.py                     # Main program entry point
├── requirements.txt           # Dependency list
├── .env.example               # Environment variable example
└── README.md                  # Project documentation
```

## 🧩 System Architecture

XianyuBot adopts a modular layered architecture design:

<table>
<tr>
<th>Layer</th>
<th>Functionality</th>
</tr>
<tr>
<td><strong>API Layer</strong></td>
<td>

- WebSocket connection maintenance
- Message sending and receiving management
- Session state monitoring

</td>
</tr>
<tr>
<td><strong>Core Layer</strong></td>
<td>

- Context Management: Records conversation history
- State Tracking: Follows transaction stages
- Message Routing: Dispatches to appropriate expert agents

</td>
</tr>
<tr>
<td><strong>Agent Layer</strong></td>
<td>

- Base Agent: Provides general conversation capabilities
- Expert Agents: Handles specific scenarios (negotiation, logistics, etc.)
- Collaborative Mechanism: Multi-expert collaborative decision-making

</td>
</tr>
<tr>
<td><strong>Tool Layer</strong></td>
<td>

- Login Management: Automatically obtains and refreshes login credentials
- Configuration Management: Flexible environment variable control

</td>
</tr>
</table>

## 📊 Performance and Limitations

| Metric | Value/Description |
|------|-----------|
| **Response Speed** | Average reply time < 3 seconds |
| **Concurrent Processing** | Single instance supports multiple concurrent sessions |
| **Memory Usage** | Approximately 150-300MB (depending on the number of active sessions) |
| **API Quota** | Depends on your OpenAI API Key limitations |

## 🐳 Docker Deployment

### Quick Start

```bash
# 1. Prepare cookies file
cp your_cookies.json data/xianyu_cookies.json

# 2. Use startup script (interactive)
chmod +x scripts/docker-start.sh
./scripts/docker-start.sh

# Or manual start
docker-compose up -d
```

### Access Services

- **Web Feedback Dashboard**: http://localhost:5000
- **View Logs**: `docker-compose logs -f`

Detailed deployment guide: [DOCKER_DEPLOY.md](./DOCKER_DEPLOY.md)

---

## 🧠 AI Training and Optimization

### Web Feedback Dashboard

After starting the web server, you can visually mark conversation outcomes:

```bash
# Start Web feedback dashboard
cd web && python feedback_server.py

# Or Docker mode
docker-compose up -d
```

Features:
- 📊 View conversation statistics reports
- 💬 Browse historical conversation records
- 🏷️ Mark conversation outcomes (deal/no_deal/ongoing)
- 📈 View AI learning effectiveness

### Command Line Feedback Tool

```bash
# View statistics
python feedback.py stats

# Mark conversation outcome
python feedback.py record <user_id> <item_id> deal <final_price> <original_price>
```

> **Tip**: Regularly mark conversation outcomes (recommended 5-10 per day) to help AI learn and optimize reply strategies faster.

---

## 🔮 Future Plans

- [x] Web management interface (visual configuration and monitoring) ✅
- [x] AI continuous learning system (feedback optimization) ✅
- [x] Docker one-click deployment ✅
- [ ] Knowledge base management (RAG support to enhance reply quality)
- [ ] Compatibility with various model backends (suggestions welcome via issues)
- [ ] Add more expert agent types
- [ ] Support for multiple accounts simultaneously online
- [ ] Mobile management App

## 🤝 Contributions and Support

Issues and Pull Requests are welcome to help improve XianyuBot! For usage problems, please submit detailed error reports on GitHub.

## 📄 License

This project is open-sourced under the MIT License.

## 🧸 Special Thanks

This project is rebuilt based on the following open-source project:
- [XianyuAutoAgent](https://github.com/shaxiu/XianyuAutoAgent) - An intelligent Xianyu customer service bot system, developed by [@shaxiu](https://github.com/shaxiu) and [@cv-cat](https://github.com/cv-cat)
</rewritten_file> 