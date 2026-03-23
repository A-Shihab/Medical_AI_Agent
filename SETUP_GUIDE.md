# 📘 Complete Setup Guide - Medical AI Agent

This guide will walk you through every step to get your Medical AI Agent running.

## 🎯 What You'll Build

A chatbot that can:
- Answer questions about medical datasets (Heart Disease, Cancer, Diabetes)
- Search the web for general medical information
- Automatically decide which source to use

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] Python 3.8 or higher installed
- [ ] Internet connection
- [ ] Text editor (VS Code, Sublime, etc.)
- [ ] Terminal/Command Prompt access

## 🔑 Step 1: Get Your API Keys (15 minutes)

### 1.1 OpenAI API Key

1. Go to https://platform.openai.com/signup
2. Create an account (or log in)
3. Go to https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. **IMPORTANT**: Copy the key immediately (you won't see it again!)
6. Keep it somewhere safe (you'll add it to .env later)

**Cost**: Pay-as-you-go. Approximately $0.01-0.05 per query with GPT-4

### 1.2 Tavily API Key (Free tier available)

1. Go to https://app.tavily.com/
2. Sign up for a free account
3. Once logged in, you'll see your API key on the dashboard
4. Copy the key

**Free tier**: 1000 searches per month

### 1.3 Kaggle API Credentials

1. Go to https://www.kaggle.com/
2. Create an account (or log in)
3. Click on your profile picture → Account
4. Scroll to "API" section
5. Click "Create New API Token"
6. This downloads `kaggle.json` file
7. Note the location of this file

## 💻 Step 2: Setup Your Environment (10 minutes)

### 2.1 Create Project Directory

```bash
# Create a new folder for the project
mkdir medical-ai-agent
cd medical-ai-agent
```

### 2.2 Create Virtual Environment (Recommended)

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` before your command prompt.

### 2.3 Install Jupyter

```bash
pip install jupyter
```

## 📥 Step 3: Get the Project Files

### Option A: Download from GitHub (if provided)

```bash
git clone <your-github-repo-url>
cd medical-ai-agent
```

### Option B: Create Files Manually

1. Create these files in your project directory:
   - `medical_ai_agent.ipynb` (the notebook)
   - `.env.template` (template for API keys)
   - `requirements.txt` (dependencies)
   - `README.md` (documentation)

2. Copy the content from the provided files

## 🔧 Step 4: Install Dependencies (5 minutes)

```bash
pip install -r requirements.txt
```

This will install:
- OpenAI library
- LangChain
- Pandas
- Gradio
- And more...

**Troubleshooting:**
- If you get errors, try: `pip install --upgrade pip`
- On Windows, if you get "Microsoft Visual C++ required": install from https://visualstudio.microsoft.com/downloads/

## 🗝️ Step 5: Setup API Keys (5 minutes)

### 5.1 Setup Kaggle Credentials

**On Windows:**
```cmd
mkdir %USERPROFILE%\.kaggle
copy kaggle.json %USERPROFILE%\.kaggle\kaggle.json
```

**On macOS/Linux:**
```bash
mkdir -p ~/.kaggle
cp ~/Downloads/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

### 5.2 Create .env File

1. Copy the template:
```bash
cp .env.template .env
```

2. Open `.env` in a text editor

3. Replace the placeholders with your actual keys:

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxx
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_key_from_json_file
```

4. Save the file

**IMPORTANT**: Never commit this file to GitHub!

## 🚀 Step 6: Run the Notebook (10 minutes)

### 6.1 Start Jupyter

```bash
jupyter notebook
```

This opens your browser automatically.

### 6.2 Open the Notebook

1. In the browser, click on `medical_ai_agent.ipynb`
2. The notebook will open

### 6.3 Run the Cells

Execute cells in order:

1. **Cell 1**: Install dependencies (if needed)
   - Wait for completion

2. **Cell 2**: Load API keys
   - Should print "✅ API Keys loaded successfully!"
   - If not, check your .env file

3. **Cell 3**: Download datasets
   - Takes 2-5 minutes
   - Downloads ~50MB of data
   - Creates `data/` folder

4. **Cell 4**: Create databases
   - Should print "✅ All databases created successfully!"
   - Creates 3 .db files

5. **Cell 5**: Explore schemas
   - Shows database structure
   - No action needed

6. **Cell 6**: Build database tools
   - Takes ~30 seconds
   - Creates SQL agents

7. **Cell 7**: Build web search tool
   - Quick setup

8. **Cell 8**: Create main agent
   - Combines all tools
   - Should print "🎉 System is ready!"

9. **Cell 9**: Run tests
   - Tests both database and web queries
   - Verify responses make sense

10. **Cell 10**: Launch Gradio UI
    - Opens chat interface
    - Accessible at http://localhost:7860
    - Share link generated if `share=True`

## 🎮 Step 7: Use the Agent

### In Gradio Interface:

1. Type your question in the chat box
2. Press Enter
3. Wait for response (5-15 seconds)

### Example Questions:

**Database queries:**
```
How many patients have heart disease?
What's the average age in the diabetes dataset?
Show me cholesterol statistics
```

**Web search queries:**
```
What is diabetes?
What are symptoms of heart disease?
How is cancer treated?
```

## 🐛 Common Issues and Solutions

### Issue 1: "Module not found"
```bash
# Solution: Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Issue 2: "Invalid API key"
```
# Solution: Check your .env file
# Make sure there are no spaces or quotes around keys
# Correct: OPENAI_API_KEY=sk-abc123
# Wrong: OPENAI_API_KEY="sk-abc123"
# Wrong: OPENAI_API_KEY = sk-abc123
```

### Issue 3: "Kaggle API error"
```bash
# Solution: Verify kaggle.json location
# Windows: C:\Users\YourName\.kaggle\kaggle.json
# Mac/Linux: ~/.kaggle/kaggle.json

# Check file exists:
ls ~/.kaggle/kaggle.json  # Mac/Linux
dir %USERPROFILE%\.kaggle\kaggle.json  # Windows
```

### Issue 4: "Database not found"
```
# Solution: Re-run database creation cells
# 1. Run Cell 3 (download datasets)
# 2. Run Cell 4 (create databases)
# 3. Check data/ folder exists
```

### Issue 5: "Rate limit exceeded"
```
# OpenAI: You've used up your API credits
# Solution: Add credits to your OpenAI account

# Tavily: Free tier limit reached
# Solution: Wait until next month or upgrade
```

### Issue 6: Slow responses
```
# Solution: Switch to GPT-3.5-turbo
# In Cell 6, change:
# model="gpt-4"  → model="gpt-3.5-turbo"
```

## 📊 Understanding the Costs

### OpenAI API
- **GPT-4**: ~$0.03 per query
- **GPT-3.5-Turbo**: ~$0.002 per query
- **Recommended**: Start with GPT-3.5-turbo

### Tavily
- **Free**: 1000 searches/month
- **Paid**: $20/month for 10,000 searches

### Total Estimated Cost
- Testing phase: $5-10
- Regular use: $20-50/month (depends on usage)

## 🔒 Security Best Practices

1. **Never commit .env to GitHub**
   ```bash
   # .gitignore already includes .env
   git status  # Verify .env is ignored
   ```

2. **Keep API keys secret**
   - Don't share them in screenshots
   - Don't paste them in public forums
   - Rotate keys if exposed

3. **Use environment variables**
   - Always load from .env
   - Never hardcode in scripts

## 📚 Next Steps

After getting it working:

1. **Customize the UI**
   - Modify Gradio interface in Cell 10
   - Add custom styling

2. **Add More Datasets**
   - Find datasets on Kaggle
   - Follow same pattern

3. **Improve Prompts**
   - Edit system prompts in Cell 8
   - Test different instructions

4. **Deploy Online**
   - Use Gradio's share link
   - Deploy to Hugging Face Spaces
   - Deploy to Railway/Render

## 🆘 Getting Help

If you're stuck:

1. **Check the README.md**
   - Contains detailed documentation

2. **Review Error Messages**
   - Copy full error message
   - Google the error
   - Check Stack Overflow

3. **Verify Setup**
   - API keys correct?
   - Files in right location?
   - Virtual environment activated?

4. **Start Fresh**
   ```bash
   # Delete data folder
   rm -rf data/
   
   # Re-run notebook from beginning
   ```

## ✅ Success Checklist

You're done when:

- [ ] All cells run without errors
- [ ] Databases created successfully
- [ ] Test queries return sensible answers
- [ ] Gradio interface loads
- [ ] You can ask questions and get responses

## 🎉 Congratulations!

You now have a working Medical AI Agent!

Next: Try the questions in the examples and explore the capabilities.

---

**Need more help?** Review the README.md file or check the inline comments in the code.
