# 📋 Quick Reference Card - Medical AI Agent

## 🚀 Quick Start (5 Steps)

```bash
# 1. Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# OR: venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup API keys (create .env file)
cp .env.template .env
# Edit .env and add your keys

# 4. Run the notebook
jupyter notebook medical_ai_agent.ipynb

# 5. Execute all cells in order
```

## 🔑 API Keys Needed

| Service | Get From | Free Tier | Cost |
|---------|----------|-----------|------|
| **OpenAI** | https://platform.openai.com/api-keys | No | $0.03/1k tokens (GPT-4) |
| **Tavily** | https://app.tavily.com/ | 1000/month | $20/month (Pro) |
| **Kaggle** | https://www.kaggle.com/settings/account | Unlimited | Free |

## 📂 Project Structure

```
medical-ai-agent/
├── 📓 medical_ai_agent.ipynb     # Main notebook (USE THIS)
├── 🐍 medical_agent.py           # Standalone script
├── 📝 README.md                   # Full documentation
├── 📦 requirements.txt            # Dependencies
├── 🔑 .env                        # Your API keys (CREATE THIS)
├── 📋 .env.template               # Template for .env
├── 🚫 .gitignore                  # Git ignore rules
├── 📚 SETUP_GUIDE.md             # Detailed setup
├── 🔄 API_ALTERNATIVES.md        # Other API options
├── 🔧 TROUBLESHOOTING.md         # Fix common issues
├── ⚡ quick_start.sh             # Auto setup (Mac/Linux)
├── ⚡ quick_start.bat            # Auto setup (Windows)
└── 📁 data/                      # Created automatically
    ├── heart_disease.db          # Heart disease database
    ├── cancer.db                 # Cancer database
    └── diabetes.db               # Diabetes database
```

## 🎯 How It Works

```
User Question
    ↓
Main AI Agent (GPT-4)
    ↓
┌─────────────────────┬───────────────────────┐
│  Database Query?    │   Web Search?         │
│  - "how many"       │   - "what is"         │
│  - "average"        │   - "symptoms"        │
│  - "statistics"     │   - "treatment"       │
│  - "count"          │   - "causes"          │
└─────────────────────┴───────────────────────┘
    ↓                         ↓
SQL Query on                Tavily Web
SQLite DBs                  Search
    ↓                         ↓
Natural Language Response
```

## 💡 Example Queries

### Database Queries (→ SQL)
```
✓ "How many patients have heart disease?"
✓ "What is the average age in the diabetes dataset?"
✓ "Show me cholesterol statistics"
✓ "Count of male vs female cancer patients"
✓ "What percentage have high blood pressure?"
```

### Web Searches (→ Tavily)
```
✓ "What is diabetes?"
✓ "What are the symptoms of heart disease?"
✓ "How is cancer treated?"
✓ "What causes high cholesterol?"
✓ "Risk factors for diabetes"
```

## 🛠️ Key Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Main Agent** | Routes queries | LangChain + GPT-4 |
| **DB Tools** | Query datasets | LangChain SQL Agent |
| **Web Tool** | Search internet | Tavily API |
| **UI** | Chat interface | Gradio |
| **Databases** | Store data | SQLite |

## 📊 Databases

| Database | Records | Key Columns |
|----------|---------|-------------|
| **Heart Disease** | ~300 | age, sex, cholesterol, heart_disease |
| **Cancer** | varies | age, tumor_size, cancer_type |
| **Diabetes** | ~768 | glucose, bmi, diabetes_outcome |

## ⚙️ Configuration

### Change LLM Model

```python
# In Cell 6:
llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # Faster, cheaper
    # OR model="gpt-4",     # Better, slower
    temperature=0
)
```

### Change Search Provider

```python
# In Cell 7:
# Current: Tavily
web_tool = MedicalWebSearchTool(api_key=TAVILY_API_KEY)

# Alternative: DuckDuckGo (Free)
from duckduckgo_search import DDGS
web_tool = DuckDuckGoSearchTool()  # No API key needed
```

### Enable Verbose Mode

```python
# In Cell 8:
self.agent_executor = AgentExecutor(
    agent=self.agent,
    tools=self.tools,
    verbose=True,  # Shows agent thinking
    max_iterations=5
)
```

## 🚨 Common Issues

| Problem | Quick Fix |
|---------|-----------|
| Module not found | `pip install -r requirements.txt` |
| Invalid API key | Check .env file format (no quotes, no spaces) |
| Kaggle error | Place kaggle.json in ~/.kaggle/ |
| Database not found | Re-run Cell 4 |
| Port in use | Change port: `demo.launch(server_port=7861)` |
| Rate limit | Wait or switch to gpt-3.5-turbo |

## 💰 Cost Estimate

### Development/Testing (100 queries)
- GPT-4: ~$3-5
- GPT-3.5-turbo: ~$0.20-0.50
- Tavily: Free (under 1000/month)

### Production (1000 queries/month)
- GPT-4: ~$30-60
- GPT-3.5-turbo: ~$2-5
- Tavily: Free or $20/month

## 🎨 Gradio Interface

```python
# Launch options:
demo.launch()                          # Local only
demo.launch(share=True)                # Public URL
demo.launch(server_port=7860)          # Specific port
demo.launch(auth=("user", "pass"))     # Password protect
```

## 🔄 Workflow

```
1. Install → 2. Config → 3. Download → 4. Create DBs → 5. Test → 6. Use
   (5 min)    (2 min)     (5 min)       (2 min)       (2 min)   (∞)
```

## 📝 File Purposes

| File | When to Use |
|------|-------------|
| **medical_ai_agent.ipynb** | Learning, development, testing |
| **medical_agent.py** | Production, deployment |
| **README.md** | First-time setup, overview |
| **SETUP_GUIDE.md** | Detailed walkthrough |
| **API_ALTERNATIVES.md** | Switching APIs, cost optimization |
| **TROUBLESHOOTING.md** | When something breaks |

## 🎯 Success Indicators

You're successful when:
- [ ] All notebook cells run without errors
- [ ] 3 .db files created in data/
- [ ] Test queries return sensible answers
- [ ] Gradio loads at localhost:7860
- [ ] Can ask questions and get responses

## 🔗 Important Links

- **OpenAI**: https://platform.openai.com/
- **Tavily**: https://app.tavily.com/
- **Kaggle**: https://www.kaggle.com/
- **LangChain Docs**: https://python.langchain.com/
- **Gradio Docs**: https://gradio.app/docs/

## 📞 Support

1. Check TROUBLESHOOTING.md
2. Read error message carefully
3. Google the error
4. Ask in LangChain Discord
5. Check GitHub issues

## 🎓 Learning Path

1. Run example queries
2. Modify prompts in Cell 8
3. Add new database
4. Try different LLMs
5. Customize Gradio UI
6. Deploy to cloud

---

**Pro Tip**: Keep this card open while working! 🚀
