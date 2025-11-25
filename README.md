# Documentation Loading Agent
## Universal Memory Bridge - Matrix Style Knowledge Loading

🚀 **Load framework documentation once, access from any AI platform**

This agent loads comprehensive framework documentation into ChromaDB, making it instantly available to:
- **Claude** (via MCP)
- **Gemini** (via API)
- **OpenAI** (via API)
- **Local LLMs** (direct ChromaDB access)
- **CrewAI agents**
- **LangChain agents**

## Full Documentation

Please see the complete project in this repository. Key files:

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project overview
- **agent.py** - Main agent implementation
- **load_frameworks.py** - Framework loading script
- **docker-compose.yml** - Complete deployment stack

## Quick Start

```bash
git clone https://github.com/devklg/doc-loading-agent.git
cd doc-loading-agent
cp .env.example .env
# Edit .env with your Context7 API key
./setup.sh setup
./setup.sh start
./setup.sh load-priority
```

## 🎯 What This Does

Load framework documentation ONCE → Store in ChromaDB → Access from ANY AI platform

**Token Efficiency**: 90% reduction (5,000 tokens → 500 tokens per query)

**Platform Agnostic**: Works with Claude, OpenAI, Gemini, local LLMs, and any agent that can query ChromaDB

## 🚀 Features

- ✅ Context7 Integration
- ✅ Docling Processing
- ✅ 17 Pre-configured Frameworks
- ✅ One-Command Deployment
- ✅ Universal AI Access
- ✅ Production Ready

---

**Created for the Universal Memory Bridge Project**

*"I know Kung Fu." - Neo*

*"I know Python, FastAPI, React, MongoDB..." - Your AI Agents* ✅
