# 🔧 Troubleshooting Guide - Medical AI Agent

This guide helps you solve common problems you might encounter.

## 🚨 Common Errors and Solutions

### 1. "ModuleNotFoundError: No module named 'X'"

**Error Message:**
```
ModuleNotFoundError: No module named 'openai'
ModuleNotFoundError: No module named 'langchain'
```

**Cause:** Package not installed or wrong environment

**Solutions:**

```bash
# Solution 1: Install missing package
pip install openai langchain

# Solution 2: Install all requirements
pip install -r requirements.txt

# Solution 3: Reinstall everything
pip install -r requirements.txt --force-reinstall

# Solution 4: Check if virtual environment is activated
# You should see (venv) in your terminal
# If not:
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 2. "Invalid API Key" or "Authentication Failed"

**Error Message:**
```
openai.error.AuthenticationError: Incorrect API key provided
Error: 401 Unauthorized
```

**Cause:** Wrong or expired API key

**Solutions:**

```bash
# Check 1: Verify .env file exists
ls -la .env  # Mac/Linux
dir .env     # Windows

# Check 2: Open .env and verify format
# Correct format (no quotes, no spaces):
OPENAI_API_KEY=sk-proj-abc123...
TAVILY_API_KEY=tvly-xyz789...

# Wrong formats:
OPENAI_API_KEY="sk-proj-abc123..."  # Remove quotes
OPENAI_API_KEY = sk-proj-abc123...  # Remove spaces around =

# Check 3: Get new API key
# OpenAI: https://platform.openai.com/api-keys
# Tavily: https://app.tavily.com/

# Check 4: Verify key is loaded
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:10])"
# Should print first 10 characters of your key
```

---

### 3. Kaggle Download Errors

**Error Message:**
```
OSError: Could not find kaggle.json
403 Forbidden
Unauthorized
```

**Cause:** Kaggle credentials not set up correctly

**Solutions:**

```bash
# Step 1: Get kaggle.json
# Go to: https://www.kaggle.com/settings/account
# Click "Create New API Token"
# Download kaggle.json

# Step 2: Place in correct location
# Mac/Linux:
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Windows:
# Place kaggle.json in C:\Users\<YourUsername>\.kaggle\

# Step 3: Verify
cat ~/.kaggle/kaggle.json  # Mac/Linux
type %USERPROFILE%\.kaggle\kaggle.json  # Windows

# Step 4: Test
kaggle datasets list
```

**Alternative - Manual Download:**

If Kaggle API doesn't work, download manually:

1. Visit dataset pages:
   - https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
   - https://www.kaggle.com/datasets/rabieelkharoua/cancer-prediction-dataset
   - https://www.kaggle.com/datasets/mathchi/diabetes-data-set

2. Click "Download" on each

3. Extract CSVs to:
   ```
   data/heart/heart.csv
   data/cancer/cancer.csv
   data/diabetes/diabetes.csv
   ```

4. Skip Cell 3 in notebook (download step)

---

### 4. "sqlite3.OperationalError: table X already exists"

**Error Message:**
```
sqlite3.OperationalError: table heart_disease already exists
```

**Cause:** Database already created

**Solutions:**

```bash
# Solution 1: Delete existing databases
rm data/*.db  # Mac/Linux
del data\*.db  # Windows

# Then re-run Cell 4

# Solution 2: Modify Cell 4
# Change:
df.to_sql(table_name, conn, if_exists='replace', index=False)
# The 'replace' option should handle this automatically
```

---

### 5. "Rate Limit Exceeded"

**Error Message:**
```
openai.error.RateLimitError: Rate limit reached
Error 429: Too Many Requests
```

**Cause:** Too many API calls too quickly

**Solutions:**

```python
# Solution 1: Add delays between calls
import time

def query_with_retry(agent, question, max_retries=3):
    for i in range(max_retries):
        try:
            return agent.query(question)
        except Exception as e:
            if "rate limit" in str(e).lower():
                wait_time = (i + 1) * 10  # 10, 20, 30 seconds
                print(f"Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    return "Error: Rate limit exceeded. Please try again later."

# Solution 2: Switch to slower but cheaper model
# In Cell 6, change:
model="gpt-3.5-turbo"  # Instead of gpt-4

# Solution 3: Check your OpenAI usage
# https://platform.openai.com/usage

# Solution 4: Upgrade your OpenAI plan
# https://platform.openai.com/account/billing
```

---

### 6. Jupyter Notebook Issues

**Error Message:**
```
Jupyter command not found
Kernel error
```

**Solutions:**

```bash
# Issue: Jupyter not installed
pip install jupyter jupyterlab

# Issue: Kernel not found
python -m ipykernel install --user --name=venv

# Issue: Notebook won't start
# Check if port 8888 is in use
jupyter notebook --port=8889

# Issue: Can't save notebook
# Check file permissions
chmod 644 medical_ai_agent.ipynb  # Mac/Linux
```

---

### 7. Gradio Interface Won't Load

**Error Message:**
```
Address already in use
Cannot connect to Gradio
```

**Solutions:**

```python
# Solution 1: Use different port
demo.launch(server_port=7861)  # Instead of 7860

# Solution 2: Kill existing process
# Mac/Linux:
lsof -ti:7860 | xargs kill -9

# Windows:
netstat -ano | findstr :7860
taskkill /PID <PID_NUMBER> /F

# Solution 3: Restart kernel
# In Jupyter: Kernel → Restart

# Solution 4: Launch without share
demo.launch(share=False)  # Faster, local only
```

---

### 8. Database Query Errors

**Error Message:**
```
sqlite3.OperationalError: no such table
pandas.errors.DatabaseError
```

**Solutions:**

```python
# Check 1: Verify database exists
import os
print(os.path.exists('data/heart_disease.db'))  # Should be True

# Check 2: Verify table exists
import sqlite3
conn = sqlite3.connect('data/heart_disease.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())  # Should show your table
conn.close()

# Check 3: Re-create database
# Re-run Cell 4 (database creation)

# Check 4: Check table name
# Ensure table_name in tool matches actual table name
```

---

### 9. Web Search Returns No Results

**Error Message:**
```
No relevant medical information found
Error performing web search
```

**Solutions:**

```python
# Check 1: Verify API key
print(os.getenv('TAVILY_API_KEY')[:10])  # Should show key

# Check 2: Test Tavily directly
from tavily import TavilyClient
client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
response = client.search(query="what is diabetes")
print(response)

# Check 3: Check quota
# Visit: https://app.tavily.com/
# Check remaining searches

# Check 4: Switch to free alternative
# Use DuckDuckGo (see API_ALTERNATIVES.md)
```

---

### 10. Memory/Performance Issues

**Error Message:**
```
MemoryError
Kernel appears to have died
System becomes slow
```

**Solutions:**

```python
# Solution 1: Use lighter model
llm = ChatOpenAI(model="gpt-3.5-turbo")  # Faster, less memory

# Solution 2: Reduce max_iterations
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=3  # Instead of 5
)

# Solution 3: Clear variables
del large_variable
import gc
gc.collect()

# Solution 4: Restart kernel
# Jupyter: Kernel → Restart & Clear Output

# Solution 5: Close other applications
# Free up RAM before running
```

---

### 11. Import Errors After Installation

**Error Message:**
```
ImportError: cannot import name 'ChatOpenAI'
AttributeError: module 'langchain' has no attribute 'X'
```

**Solutions:**

```bash
# Cause: Version mismatch or outdated packages

# Solution 1: Update all packages
pip install --upgrade openai langchain langchain-openai langchain-community

# Solution 2: Check versions
pip show langchain
pip show openai

# Solution 3: Use specific versions
pip install openai==1.12.0 langchain==0.1.9

# Solution 4: Fresh install
pip uninstall openai langchain langchain-openai langchain-community
pip install -r requirements.txt
```

---

### 12. "Can't connect to OpenAI" / Timeout Errors

**Error Message:**
```
Connection timeout
Failed to connect to api.openai.com
```

**Solutions:**

```python
# Check 1: Internet connection
import requests
response = requests.get('https://www.google.com', timeout=5)
print(response.status_code)  # Should be 200

# Check 2: OpenAI status
# Visit: https://status.openai.com/

# Check 3: Firewall/proxy
# May need to configure proxy settings

# Check 4: Increase timeout
llm = ChatOpenAI(
    model="gpt-4",
    request_timeout=60  # 60 seconds instead of default
)

# Check 5: Use VPN if region blocked
# Some countries/networks block OpenAI
```

---

## 🧪 Debugging Steps

### General Debugging Workflow

```python
# 1. Enable verbose mode
# In Cell 8, change:
verbose=True  # Shows all agent decisions

# 2. Add print statements
def query(self, question: str) -> str:
    print(f"Received question: {question}")
    try:
        result = self.agent.invoke({"input": question})
        print(f"Result: {result}")
        return result['output']
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"

# 3. Test components individually
# Test database tool
heart_tool.query("How many rows?")

# Test web search tool
web_tool.search("What is diabetes?")

# 4. Check logs
# Jupyter shows errors in cell output
# Python script shows errors in terminal
```

---

## 📊 Verification Checklist

Before asking for help, verify:

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Virtual environment activated (`which python` shows venv)
- [ ] All packages installed (`pip list | grep langchain`)
- [ ] .env file exists and has correct format (`cat .env`)
- [ ] Kaggle credentials in right place (`ls ~/.kaggle/kaggle.json`)
- [ ] Databases created (`ls data/*.db`)
- [ ] API keys are valid (test on provider website)
- [ ] Internet connection working
- [ ] Tried restarting kernel/script
- [ ] Checked for typos in code

---

## 🆘 Still Stuck?

### Getting Help

1. **Read Error Messages Carefully**
   - Copy the full error message
   - Google it with "langchain" or "openai"

2. **Check Documentation**
   - LangChain: https://python.langchain.com/
   - OpenAI: https://platform.openai.com/docs
   - Tavily: https://docs.tavily.com/

3. **Search Issues**
   - GitHub Issues for each library
   - Stack Overflow with error message

4. **Ask in Communities**
   - LangChain Discord
   - r/LangChain subreddit
   - OpenAI Community Forum

### Providing Information When Asking

Include:
1. Full error message (copy-paste, not screenshot)
2. Python version (`python --version`)
3. Package versions (`pip show langchain openai`)
4. Operating system
5. What you were trying to do
6. What you've already tried

---

## 🔄 Starting Fresh

If nothing works, start over:

```bash
# 1. Delete everything
rm -rf venv data *.db

# 2. Re-create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# 3. Fresh install
pip install --upgrade pip
pip install -r requirements.txt

# 4. Re-setup API keys
nano .env  # Add keys

# 5. Re-run notebook from Cell 1
```

This solves 80% of persistent issues!

---

**Remember:** Most issues are due to:
1. Wrong API keys (40%)
2. Missing packages (30%)
3. File locations (20%)
4. Version mismatches (10%)

Double-check these first! 🎯
