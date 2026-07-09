# 🧠 Multi-Tool Medical AI Agent

A sophisticated AI agent system that intelligently routes medical queries to appropriate data sources - either querying SQLite databases containing medical datasets (Heart Disease, Cancer, Diabetes) or searching the web for general medical knowledge.

## 🎯 Features

- **Smart Query Routing**: Automatically determines whether to query databases or search the web
- **Multi-Database Support**: Three specialized medical databases (Heart Disease, Cancer, Diabetes)
- **Natural Language Interface**: Ask questions in plain English
- **Web Search Integration**: Get up-to-date medical information from trusted sources
- **Gradio UI**: User-friendly chat interface for queries
- **SQL Agent**: Converts natural language to SQL queries automatically

## 📁 Project Structure

```
medical-ai-agent/
├── medical_ai_agent.ipynb    # Main notebook with all code
├── .env                       # Your API keys (create from .env.template)
├── .env.template              # Template for environment variables
├── README.md                  # This file
├── requirements.txt           # Python dependencies
└── data/                      # Created automatically
    ├── heart_disease.db       # Heart disease SQLite database
    ├── cancer.db              # Cancer prediction SQLite database
    ├── diabetes.db            # Diabetes SQLite database
    ├── heart/                 # Downloaded CSV files
    ├── cancer/                # Downloaded CSV files
    └── diabetes/              # Downloaded CSV files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Jupyter Notebook or JupyterLab
- Internet connection (for downloading datasets and API calls)

### Step 1: Clone and Setup

```bash
# Clone the repository (or create a new directory)
mkdir medical-ai-agent
cd medical-ai-agent

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install openai langchain langchain-openai langchain-community pandas sqlite3 kaggle python-dotenv tavily-python gradio jupyter
```

### Step 3: Setup API Keys

1. **OpenAI API Key**
   - Go to https://platform.openai.com/api-keys
   - Create a new API key
   - Copy the key

2. **Tavily API Key** (for web search)
   - Go to https://app.tavily.com/
   - Sign up for a free account
   - Get your API key from the dashboard

3. **Kaggle API Credentials**
   - Go to https://www.kaggle.com/settings/account
   - Scroll to "API" section
   - Click "Create New API Token"
   - Download `kaggle.json`
   - Place it in `~/.kaggle/` directory (create if doesn't exist)
   - On Windows: `C:\Users\<YourUsername>\.kaggle\kaggle.json`
   - On macOS/Linux: `~/.kaggle/kaggle.json`

4. **Create .env file**

Copy `.env.template` to `.env` and add your keys:

```bash
cp .env.template .env
```

Edit `.env` and replace placeholders:

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxx
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_key_from_kaggle_json
```

### Step 4: Run the Notebook

```bash
# Start Jupyter Notebook
jupyter notebook medical_ai_agent.ipynb
```

Or use JupyterLab:

```bash
jupyter lab medical_ai_agent.ipynb
```

### Step 5: Execute Cells in Order

Run each cell in the notebook sequentially:

1. **Cell 1-2**: Install dependencies and load API keys
2. **Cell 3**: Download datasets from Kaggle
3. **Cell 4**: Convert CSVs to SQLite databases
4. **Cell 5**: Explore database schemas
5. **Cell 6**: Build database-specific tools
6. **Cell 7**: Build web search tool
7. **Cell 8**: Create main AI agent
8. **Cell 9**: Test with sample queries
9. **Cell 10**: Launch Gradio interface

## 🎮 Usage Examples

### Database Queries (Statistics & Data)

```
❓ "How many patients in the heart disease dataset have heart disease?"
❓ "What is the average age of cancer patients in the dataset?"
❓ "Show me statistics about glucose levels in diabetic patients"
❓ "What percentage of patients have high cholesterol?"
❓ "Give me a count of male vs female patients with diabetes"
```

### Web Search Queries (General Knowledge)

```
❓ "What is diabetes and what are its main symptoms?"
❓ "What are the risk factors for heart disease?"
❓ "How is cancer typically treated?"
❓ "What causes high blood pressure?"
❓ "What are the early warning signs of diabetes?"
```

## 🛠️ Technical Architecture

### Components

1. **Database Tools** (`DatabaseQueryTool`)
   - HeartDiseaseDBTool
   - CancerDBTool
   - DiabetesDBTool
   - Uses LangChain SQL Agent to convert natural language to SQL

2. **Web Search Tool** (`MedicalWebSearchTool`)
   - Uses Tavily API for medical information search
   - Returns synthesized information from multiple sources

3. **Main Agent** (`MedicalAIAgent`)
   - Uses OpenAI GPT-4 for reasoning
   - Routes queries to appropriate tools
   - Synthesizes responses

### How It Works

```
User Query
    ↓
Main AI Agent (GPT-4)
    ↓
Decision: Database or Web?
    ↓
┌───────────────┬────────────────┐
│   Database    │   Web Search   │
│   Contains:   │   Contains:    │
│   - "count"   │   - "what is"  │
│   - "average" │   - "symptoms" │
│   - "stats"   │   - "treatment"│
│   - "how many"│   - "causes"   │
└───────────────┴────────────────┘
    ↓                    ↓
SQL Query          Tavily Search
    ↓                    ↓
Database Result    Web Results
    ↓                    ↓
└────────┬─────────────┘
         ↓
   Final Response
```

## 📊 Datasets

### 1. Heart Disease Dataset
- **Source**: [Kaggle - Heart Disease Dataset](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset)
- **Records**: ~300 patients
- **Features**: Age, sex, chest pain type, blood pressure, cholesterol, etc.

### 2. Cancer Prediction Dataset
- **Source**: [Kaggle - Cancer Prediction Dataset](https://www.kaggle.com/datasets/rabieelkharoua/cancer-prediction-dataset)
- **Records**: Varies by dataset
- **Features**: Patient demographics, tumor characteristics, etc.

### 3. Diabetes Dataset
- **Source**: [Kaggle - Diabetes Dataset](https://www.kaggle.com/datasets/mathchi/diabetes-data-set)
- **Records**: ~768 patients
- **Features**: Pregnancies, glucose, blood pressure, BMI, diabetes pedigree, etc.

## 🔧 Troubleshooting

### Issue: Kaggle Download Fails

**Solution**: Ensure `kaggle.json` is in the correct location:
```bash
# On macOS/Linux
mkdir -p ~/.kaggle
cp kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# On Windows
# Place kaggle.json in C:\Users\<YourUsername>\.kaggle\
```

### Issue: OpenAI API Rate Limit

**Solution**: 
- Use `gpt-3.5-turbo` instead of `gpt-4` (change in notebook)
- Add delays between requests
- Check your OpenAI usage limits

### Issue: Tavily API Limit Reached

**Solution**:
- Free tier has limited searches per month
- Consider upgrading or using alternative search APIs
- Implement caching for repeated queries

### Issue: Database Not Found

**Solution**:
- Ensure Cell 4 (database creation) runs successfully
- Check `data/` directory exists
- Verify CSV files were downloaded

## 🎨 Customization

### Adding New Databases

1. Download your dataset
2. Convert to SQLite:
```python
create_database('path/to/your.csv', 'your_db.db', 'table_name')
```
3. Create a new tool:
```python
your_tool = DatabaseQueryTool(
    db_path="data/your_db.db",
    table_name="table_name",
    description="Description for the agent"
)
```
4. Add to main agent's tools list

### Changing the LLM Model

Edit the `llm` initialization:
```python
llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # Change this
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)
```

### Using Different Search APIs

Replace Tavily with alternatives:
- **SerpAPI**: https://serpapi.com/
- **Bing Search API**: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
- **Google Custom Search**: https://developers.google.com/custom-search

## 📝 Requirements

```
openai>=1.0.0
langchain>=0.1.0
langchain-openai>=0.0.2
langchain-community>=0.0.10
pandas>=1.5.0
kaggle>=1.5.12
python-dotenv>=0.19.0
tavily-python>=0.3.0
gradio>=4.0.0
jupyter>=1.0.0
```

## 👥 Contributors

This project was collaboratively developed by:

- **Asaduzzaman Shihab**
- **Wasee Ahsan**

Both contributors participated in the design and development of the project. Individual responsibilities varied across the AI agent architecture, tool development, database integration, and documentation.

## 📄 License

This project is for educational purposes. Please ensure compliance with:
- OpenAI Terms of Service
- Kaggle Dataset Licenses
- Tavily API Terms

## 🔗 Useful Links

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [Tavily API Docs](https://docs.tavily.com/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Kaggle API Guide](https://github.com/Kaggle/kaggle-api)

## ⚠️ Important Notes

- **Medical Disclaimer**: This is an educational project. Do not use for actual medical diagnosis or treatment decisions.
- **API Costs**: OpenAI API usage incurs costs. Monitor your usage.
- **Data Privacy**: Do not upload sensitive medical data to public APIs.
- **Rate Limits**: Be aware of API rate limits for all services used.

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API documentation
3. Check tool versions compatibility

---

**Built with ❤️ for medical AI research and education**
