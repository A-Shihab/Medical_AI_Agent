"""
Medical AI Agent - Standalone Script
This script can be run directly without Jupyter Notebook
"""

import os
import sys
import pandas as pd
import sqlite3
import kaggle
from dotenv import load_dotenv
from langchain.agents import create_sql_agent, AgentExecutor, create_openai_functions_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from tavily import TavilyClient
import gradio as gr

# Load environment variables
load_dotenv()

class DatabaseSetup:
    """Setup and manage medical databases"""
    
    @staticmethod
    def download_datasets():
        """Download datasets from Kaggle"""
        print("📥 Downloading datasets from Kaggle...")
        
        os.makedirs('data/heart', exist_ok=True)
        os.makedirs('data/cancer', exist_ok=True)
        os.makedirs('data/diabetes', exist_ok=True)
        
        try:
            print("  - Downloading Heart Disease Dataset...")
            kaggle.api.dataset_download_files(
                'johnsmith88/heart-disease-dataset', 
                path='data/heart', 
                unzip=True
            )
            
            print("  - Downloading Cancer Prediction Dataset...")
            kaggle.api.dataset_download_files(
                'rabieelkharoua/cancer-prediction-dataset', 
                path='data/cancer', 
                unzip=True
            )
            
            print("  - Downloading Diabetes Dataset...")
            kaggle.api.dataset_download_files(
                'mathchi/diabetes-data-set', 
                path='data/diabetes', 
                unzip=True
            )
            
            print("✅ All datasets downloaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error downloading datasets: {str(e)}")
            print("Please ensure your Kaggle API credentials are set up correctly.")
            return False
    
    @staticmethod
    def create_database(csv_path, db_name, table_name):
        """Convert CSV to SQLite database"""
        try:
            df = pd.read_csv(csv_path)
            conn = sqlite3.connect(f'data/{db_name}')
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            print(f"✅ Created {db_name} with {count} rows in table '{table_name}'")
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error creating {db_name}: {str(e)}")
            return False
    
    @staticmethod
    def setup_all_databases():
        """Setup all medical databases"""
        print("\n🗄️ Creating SQLite databases...")
        
        import glob
        
        # Find CSV files
        heart_csv = glob.glob('data/heart/*.csv')[0]
        cancer_csv = glob.glob('data/cancer/*.csv')[0]
        diabetes_csv = glob.glob('data/diabetes/*.csv')[0]
        
        # Create databases
        DatabaseSetup.create_database(heart_csv, 'heart_disease.db', 'heart_disease')
        DatabaseSetup.create_database(cancer_csv, 'cancer.db', 'cancer_data')
        DatabaseSetup.create_database(diabetes_csv, 'diabetes.db', 'diabetes_data')
        
        print("✅ All databases created successfully!\n")


class DatabaseQueryTool:
    """Tool for querying medical databases"""
    
    def __init__(self, db_path, table_name, description, llm):
        self.db_path = db_path
        self.table_name = table_name
        self.description = description
        
        self.db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=llm)
        self.agent = create_sql_agent(
            llm=llm,
            toolkit=self.toolkit,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False  # Set to True for debugging
        )
    
    def query(self, question: str) -> str:
        """Execute a natural language query"""
        try:
            result = self.agent.invoke({"input": question})
            return result['output']
        except Exception as e:
            return f"Error querying database: {str(e)}"


class MedicalWebSearchTool:
    """Tool for searching medical information on the web"""
    
    def __init__(self, api_key):
        self.client = TavilyClient(api_key=api_key)
        self.description = "Search for general medical knowledge, definitions, symptoms, treatments"
    
    def search(self, query: str) -> str:
        """Search the web for medical information"""
        try:
            medical_query = f"medical information: {query}"
            response = self.client.search(
                query=medical_query,
                search_depth="advanced",
                max_results=5
            )
            
            results = []
            for result in response.get('results', []):
                results.append(f"**{result['title']}**\n{result['content']}\n")
            
            return "\n".join(results) if results else "No relevant medical information found."
        except Exception as e:
            return f"Error performing web search: {str(e)}"


class MedicalAIAgent:
    """Main AI Agent that routes queries to appropriate tools"""
    
    def __init__(self, heart_tool, cancer_tool, diabetes_tool, web_tool, llm):
        self.tools = [
            Tool(
                name="HeartDiseaseDBTool",
                func=heart_tool.query,
                description="""Use for heart disease statistics, patient data, and patterns. 
                Examples: 'How many patients have heart disease?', 'Average age of heart disease patients'"""
            ),
            Tool(
                name="CancerDBTool",
                func=cancer_tool.query,
                description="""Use for cancer statistics, patient data, and patterns.
                Examples: 'How many cancer cases?', 'Average age of cancer patients'"""
            ),
            Tool(
                name="DiabetesDBTool",
                func=diabetes_tool.query,
                description="""Use for diabetes statistics, patient data, and patterns.
                Examples: 'How many diabetic patients?', 'Average glucose level'"""
            ),
            Tool(
                name="MedicalWebSearchTool",
                func=web_tool.search,
                description="""Use for general medical knowledge, definitions, symptoms, treatments.
                Examples: 'What is diabetes?', 'Symptoms of heart disease', 'Cancer treatments'"""
            )
        ]
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Medical AI Assistant with access to multiple tools:

            **Database Tools**: Use when asked about statistics, data, numbers, counts, averages
            **Web Search Tool**: Use when asked about definitions, symptoms, causes, treatments, cures

            Decision Rules:
            - Words like "how many", "average", "statistics", "count" → Database
            - Words like "what is", "symptoms", "causes", "treatment" → Web Search
            
            Always provide clear, helpful answers."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.agent = create_openai_functions_agent(llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=False,  # Set to True for debugging
            handle_parsing_errors=True,
            max_iterations=5
        )
    
    def query(self, question: str) -> str:
        """Process a user query"""
        try:
            result = self.agent_executor.invoke({"input": question})
            return result['output']
        except Exception as e:
            return f"Error processing query: {str(e)}"


def initialize_system():
    """Initialize the complete medical AI agent system"""
    
    print("🚀 Initializing Medical AI Agent System...\n")
    
    # Check API keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
    
    if not OPENAI_API_KEY or not TAVILY_API_KEY:
        print("❌ Error: API keys not found!")
        print("Please create a .env file with your API keys.")
        sys.exit(1)
    
    print("✅ API keys loaded")
    
    # Check if databases exist, if not, create them
    if not os.path.exists('data/heart_disease.db'):
        print("\n📦 Databases not found. Setting up for the first time...")
        if DatabaseSetup.download_datasets():
            DatabaseSetup.setup_all_databases()
        else:
            print("❌ Failed to download datasets. Please check your Kaggle credentials.")
            sys.exit(1)
    else:
        print("✅ Databases found")
    
    # Initialize LLM
    print("\n🤖 Initializing AI models...")
    llm = ChatOpenAI(
        model="gpt-4",  # Change to "gpt-3.5-turbo" for faster/cheaper
        temperature=0,
        openai_api_key=OPENAI_API_KEY
    )
    
    # Create database tools
    print("🔧 Creating database tools...")
    heart_tool = DatabaseQueryTool(
        db_path="data/heart_disease.db",
        table_name="heart_disease",
        description="Heart disease dataset queries",
        llm=llm
    )
    
    cancer_tool = DatabaseQueryTool(
        db_path="data/cancer.db",
        table_name="cancer_data",
        description="Cancer dataset queries",
        llm=llm
    )
    
    diabetes_tool = DatabaseQueryTool(
        db_path="data/diabetes.db",
        table_name="diabetes_data",
        description="Diabetes dataset queries",
        llm=llm
    )
    
    # Create web search tool
    print("🌐 Creating web search tool...")
    web_tool = MedicalWebSearchTool(api_key=TAVILY_API_KEY)
    
    # Create main agent
    print("🧠 Creating main AI agent...")
    agent = MedicalAIAgent(heart_tool, cancer_tool, diabetes_tool, web_tool, llm)
    
    print("\n✅ System initialization complete!\n")
    
    return agent


def create_gradio_interface(agent):
    """Create Gradio chat interface"""
    
    def query_agent(message, history):
        """Process user message"""
        return agent.query(message)
    
    demo = gr.ChatInterface(
        fn=query_agent,
        title="🧠 Medical AI Agent",
        description="""Ask questions about medical data or general medical knowledge!
        
        **📊 Data Queries**: "How many patients have diabetes?", "Average age in cancer dataset?"
        **🌐 General Knowledge**: "What is hypertension?", "Symptoms of diabetes?"
        """,
        examples=[
            "How many patients in the heart disease dataset have heart disease?",
            "What is diabetes and what are its symptoms?",
            "What is the average age of cancer patients in the dataset?",
            "What are the risk factors for heart disease?",
            "Show me statistics about glucose levels in diabetic patients",
            "How is cancer typically treated?"
        ],
        theme=gr.themes.Soft(),
        retry_btn="🔄 Retry",
        undo_btn="↩️ Undo",
        clear_btn="🗑️ Clear"
    )
    
    return demo


def main():
    """Main function to run the application"""
    
    print("="*70)
    print("🧠 MEDICAL AI AGENT SYSTEM")
    print("="*70)
    
    # Initialize system
    agent = initialize_system()
    
    # Test queries (optional)
    print("🧪 Running test queries...\n")
    
    test_queries = [
        "How many patients are in the heart disease dataset?",
        "What is diabetes?"
    ]
    
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        response = agent.query(query)
        print(f"📝 Response: {response}\n")
        print("-"*70)
    
    # Launch Gradio interface
    print("\n🎨 Launching Gradio interface...")
    demo = create_gradio_interface(agent)
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
