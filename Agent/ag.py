import asyncio
import gradio as gr
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage, TextMessage
from autogen_agentchat.ui import Console
from autogen_agentchat.tools import AgentTool
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient
import datetime
import random
import os
from dotenv import load_dotenv
import whisper
import tempfile
from gtts import gTTS
import io
import warnings
import requests
import json
from docx import Document
from pathlib import Path
from tab2 import CustomerBankingAgent
from tab3 import Tab3Agent
from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain.tools.tavily_search import TavilySearchResults


# Load environment variables
load_dotenv()

# File processing function
def process_uploaded_file(file_path: str) -> str:
    """Extract content from uploaded file (txt, json, doc, docx)"""
    if not file_path or not os.path.exists(file_path):
        return "Error: File not found"
    
    try:
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        elif file_extension == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return json.dumps(data, indent=2)
                
        elif file_extension in ['.doc', '.docx']:
            try:
                doc = Document(file_path)
                content = []
                for paragraph in doc.paragraphs:
                    if paragraph.text.strip():
                        content.append(paragraph.text.strip())
                return '\n'.join(content)
            except Exception as e:
                return f"Error reading Word document: {str(e)}"
                
        else:
            return f"Unsupported file type: {file_extension}. Please upload txt, json, doc, or docx files."
            
    except Exception as e:
        return f"Error processing file: {str(e)}"

def get_yahoo_ticker(company_name: str, stock_exchange: str = None) -> dict:
    """Find ticker symbol and company name from Yahoo Finance with stock exchange support"""
    # Clean the input
    company_name = company_name.strip()
    
    # If stock exchange is specified, normalize it
    if stock_exchange:
        stock_exchange = stock_exchange.strip().upper()
        # Convert NSE to NSI (correct Yahoo Finance suffix for Indian stocks)
        if stock_exchange == "NSE":
            stock_exchange = "NS"
        elif stock_exchange == "NSI":
            stock_exchange = "NS"
    
    # Search query
    search_query = company_name
    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={search_query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {'Error': f'HTTP {response.status_code}'}
        
        results = response.json()
        if 'quotes' not in results or not results['quotes']:
            return {'Error': 'No results found'}
        
        quotes = results['quotes']
        
        # If stock exchange is specified, look for tickers with that suffix
        if stock_exchange:
            for quote in quotes:
                symbol = quote.get('symbol', '')
                name = quote.get('shortname') or quote.get('longname', '')
                exchange = quote.get('exchange', '')
                
                # Check if symbol already has the desired suffix
                if symbol.endswith(f".{stock_exchange}"):
                    return {
                        'Ticker': symbol,
                        'Name': name,
                        'Exchange': exchange,
                        'Message': f'Found ticker with {stock_exchange} exchange'
                    }
                
                # Check if we can append the suffix
                if not '.' in symbol and exchange and stock_exchange.lower() in exchange.lower():
                    ticker_with_exchange = f"{symbol}.{stock_exchange}"
                    return {
                        'Ticker': ticker_with_exchange,
                        'Name': name,
                        'Exchange': exchange,
                        'Message': f'Added {stock_exchange} suffix to ticker'
                    }
        
        # Auto-detect Indian companies for NSI suffix
        indian_keywords = ['india', 'indian', 'ltd', 'limited', 'mumbai', 'delhi', 'bangalore', 'chennai', 'hyderabad', 'pune']
        
        for quote in quotes:
            symbol = quote.get('symbol', '')
            name = quote.get('shortname') or quote.get('longname', '')
            exchange = quote.get('exchange', '')
            
            # Check if it's likely an Indian company
            is_indian_company = False
            if name:
                name_lower = name.lower()
                is_indian_company = any(keyword in name_lower for keyword in indian_keywords)
            
            # If no stock exchange specified but seems like Indian company, add .NS
            if not stock_exchange and is_indian_company and not '.' in symbol:
                ticker_with_ns = f"{symbol}.NS"
                return {
                    'Ticker': ticker_with_ns,
                    'Name': name,
                    'Exchange': exchange,
                    'Message': 'Auto-detected Indian company, added .NS suffix'
                }
            
            # Return first valid result if no specific exchange needed
            if symbol and name:
                return {
                    'Ticker': symbol,
                    'Name': name,
                    'Exchange': exchange,
                    'Message': 'Found ticker symbol'
                }
        
        # If we reach here, return the first quote anyway
        first_quote = quotes[0]
        symbol = first_quote.get('symbol', '')
        name = first_quote.get('shortname') or first_quote.get('longname', '')
        
        if symbol and name:
            return {
                'Ticker': symbol,
                'Name': name,
                'Exchange': first_quote.get('exchange', ''),
                'Message': 'Found ticker (first result)'
            }
        else:
            return {'Error': 'Incomplete data in response'}
            
    except requests.RequestException as e:
        return {'Error': f'Network error: {str(e)}'}
    except Exception as e:
        return {'Error': f'Processing error: {str(e)}'}

class VoiceFinancialAdvisorAgent:
    def __init__(self):

        tavily_api_key = os.getenv("TAVILY_API_KEY")
        tavily_search_tool = LangChainToolAdapter(
            TavilySearchResults(
                max_results=5,
                api_key=tavily_api_key
            )
        )

        
        """Initialize the FINBUZZ.AI financial advisor agent with voice capabilities"""
        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
        
        # Initialize Whisper model - suppress FP16 warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.whisper_model = whisper.load_model("medium")

        


        
        # Create the model client using OpenAIChatCompletionClient for Gemini
        self.model_client = OpenAIChatCompletionClient(
            model="gemini-2.0-flash",
            api_key=api_key,
        )

        self.Green_Investing_Bias_Agent = AssistantAgent(
            name="GreenInvestingBiasAlerts",
            description="Specialized agent for detecting portfolio sector bias, providing ESG investing guidance, and recommending sustainable investment alternatives",
            model_client=self.model_client,
            tools=[tavily_search_tool],  # Add Tavily search tool here
            reflect_on_tool_use=True,
            system_message="""You are a Green Investing and Bias Detection Expert. Your primary responsibilities are:

## 🎯 CORE FUNCTIONS:

### 1. SECTOR BIAS DETECTION & ANALYSIS:
- **Analyze portfolio composition** for sector concentration risks
- **Alert users** when >30% exposure to single sector (HIGH RISK)
- **Flag moderate risk** when >20% exposure to single sector  
- **Calculate sector allocation percentages** from provided portfolio data
- **Identify over-concentration** in specific industries (Tech, Banking, Pharma, etc.)

### 2. DIVERSIFICATION RECOMMENDATIONS:
When sector bias detected:
- **Search for alternative sectors** using Tavily search tool
- **Find specific companies** in underrepresented sectors
- **Suggest rebalancing strategies** with specific percentages
- **Recommend sector rotation** based on market conditions
- **Provide timeline** for gradual diversification

### 3. ESG & SUSTAINABLE INVESTING GUIDANCE:
- **Search for ESG-compliant companies** using Tavily search tool when requested
- **Find sustainable investment options** across different sectors
- **Identify green bonds, ESG ETFs,** and sustainable mutual funds
- **Research ESG ratings** and sustainability scores
- **Always direct users to https://www.sustainalytics.com/esg-ratings** for detailed ESG ratings

### 4. SEARCH STRATEGY & TOOL USAGE:
**When to use Tavily search:**
- User asks for ESG compliant companies
- Need to find companies in specific sectors for diversification
- Research sustainable investment alternatives
- Find current ESG ratings or green investment options
- Look for sector-specific investment opportunities

**Search query examples:**
- "ESG compliant technology companies India 2024"
- "Best sustainable consumer goods stocks"
- "Green energy companies for investment"
- "ESG rated banking stocks alternative"

## 📊 ANALYSIS FRAMEWORK:

### PORTFOLIO BIAS DETECTION:
1. **Calculate sector percentages** from portfolio data
2. **Identify concentration risks** (>20% = Moderate, >30% = High)
3. **Flag overexposure alerts** with specific recommendations
4. **Suggest optimal allocation** (max 15-20% per sector)

### ESG INTEGRATION:
1. **Search for ESG alternatives** in overconcentrated sectors
2. **Find sustainable companies** across different industries  
3. **Recommend ESG ETFs/funds** for instant diversification
4. **Direct to Sustainalytics** for comprehensive ESG ratings

## 🚨 ALERT SYSTEM:

**HIGH RISK ALERT** (>30% single sector):
- Immediate diversification required
- Search for 3-5 alternative sector options
- Provide specific rebalancing plan
- Timeline: 3-6 months for gradual shift

**MODERATE RISK ALERT** (20-30% single sector):
- Monitor and gradual diversification
- Search for 2-3 complementary sectors
- Suggest adding positions over time

## 📋 RESPONSE FORMAT:

Always structure your analysis as:

**🔍 SECTOR BIAS ANALYSIS:**
- Current sector breakdown with percentages
- Risk level assessment (Low/Moderate/High)
- Specific bias alerts if detected

**⚠️ DIVERSIFICATION ALERTS:**
- Clear explanation of concentration risks
- Immediate action items if high risk

**🌱 ESG & SUSTAINABLE RECOMMENDATIONS:**
- ESG-compliant alternatives found via search
- Sustainable investment options
- Link to Sustainalytics for detailed ratings

**📈 ACTION PLAN:**
- Specific steps for portfolio rebalancing
- Timeline for implementation
- Target allocation percentages

## 🔗 IMPORTANT REFERENCES:
- Always mention: "For detailed ESG ratings visit https://www.sustainalytics.com/esg-ratings"
- Use search results to provide current, relevant investment options
- Focus on actionable, specific recommendations

Remember: Your goal is to help users build diversified, sustainable portfolios while minimizing concentration risks."""
        )
        





        # Create the Ticker Finder Agent
        self.ticker_finder_agent = AssistantAgent(
            name="TickerFinder",
            description="A specialized agent for finding stock tickers and company information from Yahoo Finance with stock exchange support.",
            model_client=self.model_client,
            tools=[FunctionTool(get_yahoo_ticker, description="Find ticker symbol and company name from Yahoo Finance with optional stock exchange parameter")],
            system_message="""You are a specialized ticker finder agent. Your job is to help find stock ticker symbols and company information from Yahoo Finance. 

IMPORTANT GUIDELINES:
1. When users ask about INDIAN companies or mention Indian market/NSE/BSE, always use stock_exchange="NSI" parameter
2. For Indian companies, the correct Yahoo Finance suffix is .NS (not .NSE or .NSI)
3. If user explicitly mentions a stock exchange (like NSE, BSE, NYSE, NASDAQ), use that as the stock_exchange parameter
4. Use the get_yahoo_ticker function with both company_name and stock_exchange parameters when relevant

Examples:
- "ticker for Infosys" → use get_yahoo_ticker("Infosys", "NSI") → should return INFY.NS
- "ticker for Infosys NSE" → use get_yahoo_ticker("Infosys", "NSE") → should return INFY.NS  
- "Apple ticker" → use get_yahoo_ticker("Apple") → should return AAPL
- "Indian company Reliance" → use get_yahoo_ticker("Reliance", "NSI") → should return RELIANCE.NS

When responding:
1. Always show the full ticker symbol with exchange suffix when applicable
2. Provide the full company name
3. Mention the stock exchange if relevant
4. If no results found, suggest alternative search terms
5. Always be helpful and accurate with financial symbol information"""
        )
        self.Report_Generator_agent = AssistantAgent(
            name="ReportGenerator",
            description="A specialized agent for generating a professional report of the user financial info stating the Pros and Cons of the present financial Conditon of the user and what are the changes he needs to take and what are the risk he will face (or benefits he will get if financial info is good) if he continues with the present condition.",
            model_client=self.model_client,
            system_message="""You are a professional financial report generator agent, what will happen is the main agent will call you as a tool the main agent will pass the financial info that user gives to main agent, what you have to do is make a very good detailed report with calculations statistics forecast and various professional tool to analyse the overall financial information of user, you havve to write Pros and Cons of the particular financial condtion of user and tell him the potential risk (or benefit if financial info is good)with numbers, forecast that he can face if he continues with the same financial condition, also suggest him the robust changes that he can do, give actual changes not generic advice
             When you receive financial information, create a comprehensive professional report that includes:

    1. **Executive Summary** - Brief overview of financial position
    2. **Current Financial Position Analysis** - Detailed breakdown with numbers
    3. **Pros and Cons Analysis** - Clear advantages and disadvantages
    4. **Risk Assessment** - Potential risks with quantified impact
    5. **Benefits Analysis** - Potential benefits if conditions are favorable  
    6. **Actionable Recommendations** - Specific, implementable changes
    7. **Financial Forecasts** - Projected outcomes with calculations
    8. **Priority Action Items** - Step-by-step implementation plan

    Use professional formatting with:
    - Clear headers and sections
    - Tables for numerical data
    - Bullet points for recommendations
    - Calculations showing your work
    - Specific numbers, not generic advice

    Always provide concrete, actionable advice based on the actual data provided.""")
        
        self.Financial_Health_Scoring_Agent = AssistantAgent(
            name="FinancialHealthScoring",
            description="You are an agent responsible of taking all the user financial info analyse it and give a score between 0 to 100",
            model_client=self.model_client,
            reflect_on_tool_use=True,
            system_message= """
            You are a Financial Health Scoring Expert. When you receive financial data, you must:

1. **ANALYZE THE COMPLETE FINANCIAL PICTURE**:
   - Calculate debt-to-income ratios
   - Assess portfolio diversification
   - Evaluate asset allocation
   - Review investment performance
   - Check emergency fund adequacy
   - Analyze risk exposure

2. **PROVIDE A NUMERICAL SCORE (0-100)**:
   - 90-100: Excellent financial health
   - 80-89: Very good financial health  
   - 70-79: Good financial health
   - 60-69: Fair financial health
   - 50-59: Poor financial health
   - Below 50: Critical financial health

3. **DELIVER COMPREHENSIVE ANALYSIS**:
   - **Financial Health Score**: [0-100 with reasoning]
   - **Strengths**: What's working well
   - **Weaknesses**: Areas of concern
   - **Risk Assessment**: Potential financial risks
   - **Portfolio Analysis**: Investment breakdown and performance
   - **Debt Analysis**: Debt levels and interest burden
   - **Recommendations**: Specific actionable steps

4. **FORMAT YOUR RESPONSE PROFESSIONALLY**:
   - Use clear headings and bullet points
   - Include specific numbers and calculations
   - Provide concrete recommendations, not generic advice
   - Show your scoring methodology

When financial data is provided, analyze it thoroughly and respond with the complete assessment
        """
        )
        
        
        # Create AgentTool from the ticker finder agent
        self.ticker_finder_tool = AgentTool(agent=self.ticker_finder_agent)
        self.Report_Generator_tool = AgentTool(agent=self.Report_Generator_agent)
        self.Financial_Health_Scoring_tool = AgentTool(agent=self.Financial_Health_Scoring_Agent)
        self.Green_Investing_Bias_tool = AgentTool(agent=self.Green_Investing_Bias_Agent)
        
        # Store conversation history and user file content
        self.conversation_history = []
        self.user_file_content = ""  # Store uploaded file content
        
        # Create the agent with a financial advisor personality and ticker finder tool
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create the main agent with current system message"""
        return AssistantAgent(
            name="FINBUZZ_AI",
            model_client=self.model_client,
            tools=[self.ticker_finder_tool, self.Report_Generator_tool,self.Financial_Health_Scoring_tool,self.Green_Investing_Bias_tool],
            reflect_on_tool_use=True,
            system_message=self.get_enhanced_system_message()
        )
    
    def update_agent_with_file_content(self):
        """Update the agent with new system message including file content"""
        # Recreate the agent with updated system message
        self.agent = self._create_agent()
    
    def transcribe_audio(self, audio_file):
        """Transcribe audio using Whisper"""
        try:
            if audio_file is None or not os.path.exists(audio_file):
                return "Error: No audio file provided or file doesn't exist"
            
            # Suppress FP16 warnings during transcription
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                result = self.whisper_model.transcribe(audio_file, fp16=False)
            
            transcribed_text = result["text"].strip()
            if not transcribed_text:
                return "Error: No speech detected in audio"
            
            return transcribed_text
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            return f"Error transcribing audio: {str(e)}"
    
    def text_to_speech(self, text):
        """Convert text to speech using gTTS"""
        try:
            if not text or not text.strip():
                return None
            
            # Clean text for TTS
            clean_text = text.strip()
            if len(clean_text) > 500:  # Limit text length for TTS
                clean_text = clean_text[:500] + "..."
            
            tts = gTTS(text=clean_text, lang='en', slow=False)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                tts.save(temp_file.name)
                return temp_file.name
                
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
            return None
    
    async def generate_financial_advice(self, user_input="Hello"):
        """Generate financial advice response"""
        try:
            # Create a message
            message = TextMessage(content=user_input, source="user")
            
            # Get response from agent
            response = await self.agent.on_messages([message], cancellation_token=None)
            
            if response and response.chat_message:
                bot_response = response.chat_message.content
                
                # Store in history
                self.conversation_history.append(("user", user_input))
                self.conversation_history.append(("bot", bot_response))
                
                return bot_response
            else:
                return "I'm currently analyzing market conditions. Please try again! 📊"
                
        except Exception as e:
            return f"Market volatility detected in my circuits: {str(e)} 📈"
    
    def add_user_file_content(self, file_path):
        """Process and store user uploaded file content"""
        try:
            content = process_uploaded_file(file_path)
            if not content.startswith("Error"):
                self.user_file_content = content
                # Update the agent with new file content
                self.update_agent_with_file_content()
                return f"✅ File processed successfully! Financial information has been added to my knowledge base and I'm ready to provide personalized advice."
            else:
                return content
        except Exception as e:
            return f"❌ Error processing file: {str(e)}"
    
    def get_enhanced_system_message(self):
        """Get system message with user file content if available"""
        base_message = """You are FINBUZZ.AI, a professional and knowledgeable personal financial advisor AI assistant. 

Your personality traits:
- Provide expert financial advice and market insights
- You can give a detailed analysis report of the user's financial information explaining the pros and cons of their current financial condition, changes and results that user can face with current financial condition.
- Explain complex financial concepts in simple, understandable terms
- Offer personalized investment strategies and portfolio recommendations
- Help with budgeting, saving, debt management, and retirement planning
- Always emphasize risk management and diversification
- Provide educational content about stocks, bonds, mutual funds, ETFs, and other investment vehicles
- Maintain a professional yet approachable tone
- Ask relevant follow-up questions to better understand the user's financial goals and risk tolerance

When user requests a financial report:
1. Use the ReportGenerator tool by passing the user's financial data
2. Wait for the tool's response 
3. Present the generated report professionally
4. Do NOT use print statements or incorrect API calls

- You now have access to a ticker finder tool that can help you find stock ticker symbols and company information from Yahoo Finance. When users ask about Indian companies or mention Indian stock exchanges (NSE/BSE), make sure to specify the stock exchange parameter to get the correct .NS suffix.

Examples of how to handle requests:
- "Infosys ticker" → Use ticker finder with NSI exchange → INFY.NS
- "What's the ticker for Reliance Industries?" → Use ticker finder with NSI exchange → RELIANCE.NS  
- "Apple stock symbol" → Use ticker finder without exchange → AAPL
- "Microsoft ticker NYSE" → Use ticker finder with NYSE exchange

- You have a tool named ReportGenerator that can generate a professional report of the user's financial information. 
    
    IMPORTANT: When using the ReportGenerator tool:
    1. Pass the user's financial data as a clear, structured summary
    2. Do NOT use print() statements or incorrect syntax
    3. Simply call the tool with the financial information
    4. Present the generated report professionally
    
    Example usage: When user asks for a financial report, extract their financial data and pass it to ReportGenerator as structured text.

**FINANCIAL HEALTH SCORING - IMPORTANT INSTRUCTIONS:**

You have access to a Financial_Health_Scoring_tool that provides comprehensive financial health analysis.

**WHEN TO USE THE SCORING TOOL:**
- When user provides complete financial information (assets, liabilities, investments, etc.)
- When user asks for financial health assessment, portfolio analysis, or financial score
- When user wants to know their financial strengths/weaknesses
- When user asks "how is my financial health" or similar questions

**HOW TO USE THE SCORING TOOL:**
1. **Detect** when user has provided financial information or asks for financial health analysis
2. **Extract** all relevant financial data from the conversation
3. **Format** the data clearly and pass it to the Financial_Health_Scoring_tool
4. **Present** the complete analysis from the scoring tool to the user

**🌱 GREEN INVESTING & BIAS ALERTS - CRITICAL INSTRUCTIONS:**

You have access to a Green_Investing_Bias_tool that provides sector bias detection and ESG investing guidance.

**WHEN TO USE THE GREEN INVESTING BIAS TOOL:**
- When user provides portfolio information (automatically analyze for sector bias)
- When user asks about diversification or sector concentration
- When user mentions ESG, sustainable investing, or green investments
- When user asks for portfolio risk assessment
- When portfolio shows >20% concentration in any single sector
- When user wants alternatives to current holdings

**WHAT THE TOOL PROVIDES:**
- **Sector Bias Detection**: Identifies concentration risks in portfolio
- **Diversification Alerts**: Flags overexposure to specific sectors  
- **ESG Recommendations**: Searches for sustainable investment alternatives
- **Risk Assessment**: Analyzes concentration risks (Low/Moderate/High)
- **Action Plans**: Specific steps for portfolio rebalancing

**HOW TO USE THE GREEN INVESTING BIAS TOOL:**
1. **Automatically trigger** when portfolio data is provided
2. **Pass complete portfolio information** including all holdings and values
3. **Request specific analysis** when user asks about:
   - "Is my portfolio diversified?"
   - "ESG investment options"
   - "Sustainable companies"
   - "Portfolio sector analysis"
   - "Green investment alternatives"

**EXAMPLE TRIGGER PHRASES:**
- "Analyze my portfolio diversification"
- "Is my portfolio too concentrated?"
- "Show me ESG investment options"
- "Find sustainable alternatives to my holdings"
- "Check my sector allocation"
- "Green investing recommendations"

**INTEGRATION WITH OTHER TOOLS:**
- Use AFTER Financial Health Scoring for complete analysis
- Combine with portfolio reports for comprehensive assessment
- Cross-reference with ticker finder for specific company research

**ESG RESOURCE:**
- Always mention Sustainalytics (https://www.sustainalytics.com/esg-ratings) for detailed ESG ratings
- The tool will search for current ESG-compliant companies and sustainable investment options

**AUTOMATIC PORTFOLIO ANALYSIS:**
Whenever a user provides portfolio information, automatically:
1. Run Financial Health Scoring
2. Run Green Investing Bias Analysis  
3. Provide comprehensive report combining both analyses

This ensures users get complete portfolio assessment including financial health AND diversification/ESG analysis.
"""

        if self.user_file_content:
            base_message += f"""

IMPORTANT: The user has provided additional financial information in an uploaded file. Use this information when relevant to provide personalized advice:

USER'S FINANCIAL INFORMATION:
{self.user_file_content}

When providing advice, consider this personal financial data and reference it when appropriate to give more tailored recommendations.

**AUTOMATIC COMPREHENSIVE ANALYSIS:**
Since the user has uploaded financial information, you should automatically:
1. Use the Financial_Health_Scoring_tool for financial health analysis
2. Use the Green_Investing_Bias_tool for sector bias and ESG analysis
3. Provide a complete portfolio assessment combining both analyses

IMPORTANT FORMATTING INSTRUCTION: When displaying financial information in tabular format, create a clean, well-structured presentation using the actual user's data. Follow these formatting principles:

1. Use clear headers with emojis (📊, 💰, 💳, 📈, 🌱)
2. Group similar items together (Mutual Funds, Stocks, etc.)
3. Use proper spacing and alignment
4. Include totals and key metrics
5. Use simple text formatting with pipes (|) for column separation
6. Make it easy to read and professional looking
7. NEVER use placeholder text - always use the actual financial data from the user's file
8. Calculate accurate totals and percentages from the real data
9. Present information in a logical, hierarchical structure
10. Include sector breakdown and ESG analysis

Focus on clarity, accuracy, and professional presentation of the user's actual financial information."""


        base_message += "\n\nRemember: Your goal is to empower users with financial knowledge and help them make informed financial decisions!"
        
        
        return base_message

def create_gradio_interface():
    """Create a beautiful Gradio interface for the voice-enabled financial advisor agent"""
    
    # Initialize the agent (uses GEMINI_API_KEY from .env)
    try:
        financial_agent = VoiceFinancialAdvisorAgent()
    # ADD THIS LINE - Initialize Tab 2 agent
        customer_banking_agent = CustomerBankingAgent()
    # ADD THIS LINE - Initialize Tab 3 agent
        tab3_agent = Tab3Agent()
    except ValueError as e:
        print(f"Error: {e}")
        return None
    
    # Custom CSS for beautiful dark styling with orange accents
    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
    
    .gradio-container {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
        min-height: 100vh;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .main-header {
        text-align: center;
        color: #ffffff;
        font-size: 2.8em;
        font-weight: 700;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        margin-bottom: 20px;
        letter-spacing: -0.02em;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .chat-container {
        background: rgba(45, 45, 45, 0.95);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 138, 0, 0.2);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .custom-chatbot {
        border-radius: 15px;
        border: 1px solid rgba(255, 138, 0, 0.3);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        background: rgba(26, 26, 26, 0.8);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .custom-textbox {
        border-radius: 25px;
        border: 2px solid #ff8a00;
        padding: 12px 20px;
        background: rgba(26, 26, 26, 0.9);
        color: white;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .custom-textbox:focus {
        border-color: #ffaa33;
        box-shadow: 0 0 15px rgba(255, 138, 0, 0.3);
    }
    
    .custom-button {
        background: linear-gradient(45deg, #ff8a00, #ffaa33);
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        padding: 12px 25px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 138, 0, 0.3);
        font-family: 'JetBrains Mono', monospace;
        margin: 5px;
    }
    
    .custom-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 138, 0, 0.4);
        background: linear-gradient(45deg, #ffaa33, #ff8a00);
    }
    
    .voice-button {
        background: linear-gradient(45deg, #28a745, #20c997);
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        padding: 12px 25px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        font-family: 'JetBrains Mono', monospace;
        margin: 5px;
    }
    
    .voice-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
        background: linear-gradient(45deg, #20c997, #28a745);
    }
    
    .recording-button {
        background: linear-gradient(45deg, #dc3545, #e74c3c);
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        padding: 12px 25px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
        font-family: 'JetBrains Mono', monospace;
        margin: 5px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .voice-mode-section {
        background: rgba(45, 45, 45, 0.8);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        color: white;
        border: 1px solid rgba(255, 138, 0, 0.2);
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .control-panel {
        background: rgba(45, 45, 45, 0.8);
        border-radius: 15px;
        padding: 20px;
        color: white;
        border: 1px solid rgba(255, 138, 0, 0.2);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .button-row {
        display: flex;
        gap: 10px;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        margin: 10px 0;
    }
    
    /* Apply JetBrains Mono to all text elements */
    * {
        font-family: 'JetBrains Mono', monospace !important;
    }
    """


    async def handle_voice_input_tab3(audio_file, history, voice_chat_mode):
        if audio_file is None:
            return history, None,
        try:
            print(f"Processing audio file for Tab 3: {audio_file}")
            if not os.path.exists(audio_file):
                return history, None, "Audio file not found."
            transcribed_text = financial_agent.transcribe_audio(audio_file)
            print(f"Transcribed text: {transcribed_text}")

            if not transcribed_text or transcribed_text.startswith("Error"):
                return history, None, f"Transcription failed: {transcribed_text}"
            response = await tab3_agent.generate_response(transcribed_text)
            print(f"Tab 3 AI Response: {response}")

            if history is None:
                history = []
            history.append([transcribed_text, response])

            audio_response = None
            if voice_chat_mode:
                print("Generating voice response for Tab 3...")
                audio_response = financial_agent.text_to_speech(response)
                if audio_response:
                    print(f"Voice response generated: {audio_response}")
                else:
                    print("Failed to generate voice response")
            return history, audio_response, f"✅ Transcribed: {transcribed_text}"
        except Exception as e:
            print(f"Error in handle_voice_input_tab3: {str(e)}")
            return history, None, f"Error processing voice: {str(e)}"
        
    async def handle_text_input_tab3(message, history):
        if not message.strip():
            return history,
        response = await tab3_agent.generate_response(message)
        if history is None:
            history = []
        history.append([message, response])

        return history, ""
    
    def handle_voice_reply_tab3(history, voice_chat_mode):
        if not history or voice_chat_mode:
            return None
        try:
            last_response = history[-1][1] if history else ""
            if last_response:
                print(f"Generating voice reply for Tab 3: {last_response[:50]}...")
                audio_file = financial_agent.text_to_speech(last_response)
                if audio_file:
                    print(f"Voice reply generated: {audio_file}")
                    return audio_file
                else:
                    print("Failed to generate voice reply")
            return None
        except Exception as e:
            print(f"Error generating voice reply: {str(e)}")
            return None
        
    def handle_clear_tab3():
        tab3_agent.clear_history()
        return [], 

    def handle_file_upload_tab3(uploaded_file):
        if uploaded_file is None:
            return "Please select a file to upload."
        try:
            content = tab3_agent.process_uploaded_file(uploaded_file.name)
            if not content.startswith("Error"):
                result = asyncio.run(tab3_agent.add_user_file_content(content))
                return result
            else:
                return content
        except Exception as e:
            return f"❌ Error processing file: {str(e)}"
        
    


        




    
    async def handle_voice_input(audio_file, history, voice_chat_mode):
        """Handle voice input from microphone"""
        if audio_file is None:
            return history, None, "No audio recorded. Please record your voice first."
        
        try:
            print(f"Processing audio file: {audio_file}")
            
            # Check if file exists
            if not os.path.exists(audio_file):
                return history, None, "Audio file not found."
            
            # Transcribe audio
            transcribed_text = financial_agent.transcribe_audio(audio_file)
            print(f"Transcribed text: {transcribed_text}")
            
            if not transcribed_text or transcribed_text.startswith("Error"):
                return history, None, f"Transcription failed: {transcribed_text}"
            
            # Get AI response
            response = await financial_agent.generate_financial_advice(transcribed_text)
            print(f"AI Response: {response}")
            
            # Update chat history
            if history is None:
                history = []
            history.append([transcribed_text, response])
            
            # Generate voice response if in voice-chat mode
            audio_response = None
            if voice_chat_mode:
                print("Generating voice response...")
                audio_response = financial_agent.text_to_speech(response)
                if audio_response:
                    print(f"Voice response generated: {audio_response}")
                else:
                    print("Failed to generate voice response")
            
            return history, audio_response, f"✅ Transcribed: {transcribed_text}"
            
        except Exception as e:
            print(f"Error in handle_voice_input: {str(e)}")
            return history, None, f"Error processing voice: {str(e)}"
    
    async def handle_text_input(message, history):
        """Handle text input"""
        if not message.strip():
            return history, ""
        
        # Generate response
        response = await financial_agent.generate_financial_advice(message)
        
        # Update history
        if history is None:
            history = []
        history.append([message, response])
        
        return history, ""
    
    def handle_voice_reply(history, voice_chat_mode):
        """Generate voice reply for the last bot response"""
        if not history or voice_chat_mode:
            return None
        
        try:
            last_response = history[-1][1] if history else ""
            if last_response:
                print(f"Generating voice reply for: {last_response[:50]}...")
                audio_file = financial_agent.text_to_speech(last_response)
                if audio_file:
                    print(f"Voice reply generated: {audio_file}")
                    return audio_file
                else:
                    print("Failed to generate voice reply")
            return None
        except Exception as e:
            print(f"Error generating voice reply: {str(e)}")
            return None
    
    def handle_clear():
        """Clear conversation history"""
        financial_agent.conversation_history = []
        return [], ""
    
    def handle_file_upload(uploaded_file):
        """Handle file upload and processing"""
        if uploaded_file is None:
            return "Please select a file to upload."
        
        try:
            result = financial_agent.add_user_file_content(uploaded_file.name)
            return result
        except Exception as e:
            return f"❌ Error processing file: {str(e)}"
    
    def handle_add_file_click():
        """Handle Add File button click"""
        return "Please use the file upload section in the control panel to add your financial documents."
    
    def get_random_prompt():
        """Generate random financial conversation starters"""
        prompts = [
            "How should I start investing with $1000?",
            "Explain the difference between stocks and bonds",
            "What's a good emergency fund strategy?",
            "How do I plan for retirement in my 20s?",
            "What are the risks of cryptocurrency?",
            "How can I improve my credit score?",
            "What's dollar-cost averaging?",
            "Should I pay off debt or invest first?"
        ]
        return random.choice(prompts)
    
    async def handle_voice_input_tab2(audio_file, history, voice_chat_mode):
        """Handle voice input from microphone for Tab 2"""
        if audio_file is None:
            return history, None, "No audio recorded. Please record your voice first."
        
        try:
            print(f"Processing audio file for Tab 2: {audio_file}")
            
            if not os.path.exists(audio_file):
                return history, None, "Audio file not found."
            
            # Transcribe audio using the same whisper model from financial_agent
            transcribed_text = financial_agent.transcribe_audio(audio_file)
            print(f"Transcribed text: {transcribed_text}")
            
            if not transcribed_text or transcribed_text.startswith("Error"):
                return history, None, f"Transcription failed: {transcribed_text}"
            
            # Get AI response from Tab 2 agent
            response = await customer_banking_agent.generate_response(transcribed_text)
            print(f"Tab 2 AI Response: {response}")
            
            # Update chat history
            if history is None:
                history = []
            history.append([transcribed_text, response])
            
            # Generate voice response if in voice-chat mode
            audio_response = None
            if voice_chat_mode:
                print("Generating voice response for Tab 2...")
                audio_response = financial_agent.text_to_speech(response)
                if audio_response:
                    print(f"Voice response generated: {audio_response}")
                else:
                    print("Failed to generate voice response")
            
            return history, audio_response, f"✅ Transcribed: {transcribed_text}"
            
        except Exception as e:
            print(f"Error in handle_voice_input_tab2: {str(e)}")
            return history, None, f"Error processing voice: {str(e)}"
    
    async def handle_text_input_tab2(message, history):
        """Handle text input for Tab 2"""
        if not message.strip():
            return history, ""
        
        # Generate response from Tab 2 agent
        response = await customer_banking_agent.generate_response(message)
        
        # Update history
        if history is None:
            history = []
        history.append([message, response])
        
        return history, ""
    
    def handle_voice_reply_tab2(history, voice_chat_mode):
        """Generate voice reply for the last bot response in Tab 2"""
        if not history or voice_chat_mode:
            return None
        
        try:
            last_response = history[-1][1] if history else ""
            if last_response:
                print(f"Generating voice reply for Tab 2: {last_response[:50]}...")
                audio_file = financial_agent.text_to_speech(last_response)
                if audio_file:
                    print(f"Voice reply generated: {audio_file}")
                    return audio_file
                else:
                    print("Failed to generate voice reply")
            return None
        except Exception as e:
            print(f"Error generating voice reply: {str(e)}")
            return None
    
    def handle_clear_tab2():
        """Clear conversation history for Tab 2"""
        customer_banking_agent.clear_history()
        return [], ""
    
    def handle_file_upload_tab2(uploaded_file):
        """Handle file upload and processing for Tab 2"""
        if uploaded_file is None:
            return "Please select a file to upload."
        
        try:
            # Process file content
            content = process_uploaded_file(uploaded_file.name)
            if not content.startswith("Error"):
                result = customer_banking_agent.add_user_file_content(content)
                return result
            else:
                return content
        except Exception as e:
            return f"❌ Error processing file: {str(e)}"


    








    
    # Create the Gradio interface
    with gr.Blocks(css=custom_css, title="FINBUZZ.AI - Voice & Chat Financial Advisor") as interface:
        
        # Header without icon
        gr.HTML("""
            <div class="main-header">
                <div style="display: flex; align-items: center; justify-content: center;">
                    <span>FINBUZZ.AI</span>
                </div>
            </div>
        """)
        
        # Create tabs
        with gr.Tabs():
            with gr.TabItem("TAB 1"):
                with gr.Row():
                    with gr.Column(scale=4):  # Main chat area takes more space
                        # Voice-Chat Mode Toggle
                        with gr.Group(elem_classes="voice-mode-section"):
                            gr.HTML("<h3 style='color: #ff8a00; margin: 0;'>🎤 Voice-Chat Mode</h3>")
                            voice_chat_mode = gr.Checkbox(
                                label="Enable automatic voice replies",
                                value=False,
                                elem_id="voice-chat-toggle"
                            )
                        
                        # Main chat interface
                        with gr.Group(elem_classes="chat-container"):
                            chatbot = gr.Chatbot(
                                value=[],
                                height=600,
                                show_label=False,
                                container=False,
                                elem_classes="custom-chatbot",
                                avatar_images=(None, "finbuzz.png")
                            )
                            
                            # Text input row
                            with gr.Row():
                                msg_input = gr.Textbox(
                                    placeholder="Type your message here... 💬",
                                    show_label=False,
                                    container=False,
                                    scale=4,
                                    elem_classes="custom-textbox"
                                )
                                send_btn = gr.Button(
                                    "Send 📤", 
                                    scale=1,
                                    elem_classes="custom-button"
                                )
                    
                    with gr.Column(scale=1):  # Control panel reduced to 1/5th width
                        # Control panel
                        with gr.Group(elem_classes="control-panel"):
                            gr.HTML("""
                                <div style="text-align: center; margin-bottom: 15px;">
                                    <h3 style="color: #ff8a00; margin: 0;">🎛️ Controls</h3>
                                </div>
                            """)
                            
                            # File upload section
                            gr.HTML("<h4 style='color: #ff8a00; text-align: center;'>📁 File Upload</h4>")
                            
                            file_upload = gr.File(
                                label="Upload your financial documents (txt, json, doc, docx)",
                                file_types=[".txt", ".json", ".doc", ".docx"],
                                elem_id="file-upload"
                            )
                            
                            with gr.Row(elem_classes="button-row"):
                                process_file_btn = gr.Button(
                                    "📄 Process File",
                                    elem_classes="custom-button"
                                )
                            
                            # Voice input section
                            gr.HTML("<h4 style='color: #20c997; text-align: center;'>🎤 Voice Input</h4>")
                            
                            audio_input = gr.Audio(
                                sources=["microphone"],
                                type="filepath",
                                label="Record your question",
                                elem_id="audio-input"
                            )
                            
                            # Button row for voice controls
                            with gr.Row(elem_classes="button-row"):
                                process_voice_btn = gr.Button(
                                    "🎯 Process Voice",
                                    elem_classes="voice-button"
                                )
                            
                            # Voice output section
                            gr.HTML("<h4 style='color: #28a745; text-align: center;'>🔊 Voice Output</h4>")
                            
                            audio_output = gr.Audio(
                                label="AI Voice Response",
                                autoplay=True,
                                elem_id="audio-output"
                            )
                            
                            with gr.Row(elem_classes="button-row"):
                                voice_reply_btn = gr.Button(
                                    "🔊 Voice Reply",
                                    elem_classes="voice-button"
                                )
                            
                            # Other controls
                            gr.HTML("<h4 style='color: #ff8a00; text-align: center;'>⚙️ Other</h4>")
                            
                            with gr.Row(elem_classes="button-row"):
                                clear_btn = gr.Button(
                                    "🗑️ Clear Chat",
                                    elem_classes="custom-button"
                                )
                            
                            # Status display
                            status_display = gr.Textbox(
                                label="Status",
                                value="Ready to chat! 🚀",
                                interactive=False,
                                elem_id="status"
                            )
            
            with gr.TabItem("TAB 2"):
                with gr.Row():
                    with gr.Column(scale=4):  # Main chat area takes more space
                        # Voice-Chat Mode Toggle
                        with gr.Group(elem_classes="voice-mode-section"):
                            gr.HTML("<h3 style='color: #ff8a00; margin: 0;'>🎤 Voice-Chat Mode</h3>")
                            voice_chat_mode_tab2 = gr.Checkbox(
                                label="Enable automatic voice replies",
                                value=False,
                                elem_id="voice-chat-toggle-tab2"
                            )
                        
                        # Main chat interface
                        with gr.Group(elem_classes="chat-container"):
                            chatbot_tab2 = gr.Chatbot(
                                value=[],
                                height=600,
                                show_label=False,
                                container=False,
                                elem_classes="custom-chatbot",
                                avatar_images=(None, "finbuzz.png")
                            )
                            
                            # Text input row
                            with gr.Row():
                                msg_input_tab2 = gr.Textbox(
                                    placeholder="Ask me about banking services, fraud detection, transactions... 🏦",
                                    show_label=False,
                                    container=False,
                                    scale=4,
                                    elem_classes="custom-textbox"
                                )
                                send_btn_tab2 = gr.Button(
                                    "Send 📤", 
                                    scale=1,
                                    elem_classes="custom-button"
                                )
                    
                    with gr.Column(scale=1):  # Control panel
                        # Control panel
                        with gr.Group(elem_classes="control-panel"):
                            gr.HTML("""
                                <div style="text-align: center; margin-bottom: 15px;">
                                    <h3 style="color: #ff8a00; margin: 0;">🎛️ Controls</h3>
                                    <p style="color: #cccccc; font-size: 0.9em; margin: 5px 0;">Customer Banking Services</p>
                                </div>
                            """)
                            
                            # File upload section
                            gr.HTML("<h4 style='color: #ff8a00; text-align: center;'>📁 File Upload</h4>")
                            
                            file_upload_tab2 = gr.File(
                                label="Upload your banking documents (txt, json, doc, docx)",
                                file_types=[".txt", ".json", ".doc", ".docx"],
                                elem_id="file-upload-tab2"
                            )
                            
                            with gr.Row(elem_classes="button-row"):
                                process_file_btn_tab2 = gr.Button(
                                    "📄 Process File",
                                    elem_classes="custom-button"
                                )
                            
                            # Voice input section
                            gr.HTML("<h4 style='color: #20c997; text-align: center;'>🎤 Voice Input</h4>")
                            
                            audio_input_tab2 = gr.Audio(
                                sources=["microphone"],
                                type="filepath",
                                label="Record your banking question",
                                elem_id="audio-input-tab2"
                            )
                            
                            # Button row for voice controls
                            with gr.Row(elem_classes="button-row"):
                                process_voice_btn_tab2 = gr.Button(
                                    "🎯 Process Voice",
                                    elem_classes="voice-button"
                                )
                            
                            # Voice output section
                            gr.HTML("<h4 style='color: #28a745; text-align: center;'>🔊 Voice Output</h4>")
                            
                            audio_output_tab2 = gr.Audio(
                                label="Banking AI Voice Response",
                                autoplay=True,
                                elem_id="audio-output-tab2"
                            )
                            
                            with gr.Row(elem_classes="button-row"):
                                voice_reply_btn_tab2 = gr.Button(
                                    "🔊 Voice Reply",
                                    elem_classes="voice-button"
                                )
                            
                            # Other controls
                            gr.HTML("<h4 style='color: #ff8a00; text-align: center;'>⚙️ Other</h4>")
                            
                            with gr.Row(elem_classes="button-row"):
                                clear_btn_tab2 = gr.Button(
                                    "🗑️ Clear Chat",
                                    elem_classes="custom-button"
                                )
                            
                            # Status display
                            status_display_tab2 = gr.Textbox(
                                label="Status",
                                value="Ready to assist with banking services! 🏦",
                                interactive=False,
                                elem_id="status-tab2"
                            )
            
            with gr.TabItem("TAB 3"):
                with gr.Row():
                    with gr.Column(scale=4):
                        with gr.Group(elem_classes="voice-mode-section"):
                            gr.HTML("<h3 style='color: #ff8a00; margin: 0;'>🎤 Voice-Chat Mode</h3>")
                            voice_chat_mode_tab3 = gr.Checkbox(
                    label="Enable automatic voice replies",
                    value=False,
                    elem_id="voice-chat-toggle-tab3"
                )

                        with gr.Group(elem_classes="chat-container"):
                            chatbot_tab3 = gr.Chatbot(
                    value=[],
                    height=600,
                    show_label=False,
                    container=False,
                    elem_classes="custom-chatbot",
                    avatar_images=(None, "finbuzz.png")
                )
                            with gr.Row():
                                msg_input_tab3 = gr.Textbox(
                        placeholder="Ask me about advanced financial analysis, forecasting, sentiment... 📈",
                        show_label=False,
                        container=False,
                        scale=4,
                        elem_classes="custom-textbox"
                    )
                                send_btn_tab3 = gr.Button(
                        "Send 📤", 
                        scale=1,
                        elem_classes="custom-button"
                    )
                    
                    with gr.Column(scale=1):
                        with gr.Group(elem_classes="control-panel"):
                            gr.HTML("""
                    <div style="text-align: center; margin-bottom: 15px;">
                        <h3 style="color: #ff8a00; margin: 0;">🎛️ Controls</h3>
                        <p style="color: #cccccc; font-size: 0.9em; margin: 5px 0;">Advanced Financial Analysis</p>
                    </div>
                """)
                            gr.HTML("<h4 style='color: #ff8a00; text-align: center;'>📁 File Upload</h4>")

                            file_upload_tab3 = gr.File(
                            label="Upload your financial documents (txt, json, doc, docx)",
                            file_types=[".txt", ".json", ".doc", ".docx"],
                            elem_id="file-upload-tab3"
                )
                            with gr.Row(elem_classes="button-row"):
                                process_file_btn_tab3 = gr.Button(
                                    "📄 Process File",
                                    elem_classes="custom-button"
                                )
                            gr.HTML("<h4 style='color: #20c997; text-align: center;'>🎤 Voice Input</h4>")
                            audio_input_tab3 = gr.Audio(
                            sources=["microphone"],
                            type="filepath",
                            label="Record your financial question",
                            elem_id="audio-input-tab3"
               )
                            with gr.Row(elem_classes="button-row"):
                                process_voice_btn_tab3 = gr.Button(
                                "🎯 Process Voice",
                                elem_classes="voice-button"
                   )
                            gr.HTML("<h4 style='color: #28a745; text-align: center;'>🔊 Voice Output</h4>")
                            audio_output_tab3 = gr.Audio(
                   label="Financial AI Voice Response",
                   autoplay=True,
                   elem_id="audio-output-tab3"
               )
                            with gr.Row(elem_classes="button-row"): 
                                voice_reply_btn_tab3 = gr.Button(
                                        "🔊 Voice Reply",
                                    elem_classes="voice-button"
                   )
                            gr.HTML("<h4 style='color: #ff8a00; text-align: center;'>⚙️ Other</h4>")

                            with gr.Row(elem_classes="button-row"):
                                clear_btn_tab3 = gr.Button(
                                        "🗑️ Clear Chat",
                                    elem_classes="custom-button"
                   )
                            status_display_tab3 = gr.Textbox(
                   label="Status",
                   value="Ready for advanced financial analysis! 📈",
                   interactive=False,
                   elem_id="status-tab3"
               )






            
            with gr.TabItem("TAB 4"):
                with gr.Group(elem_classes="chat-container"):
                    gr.HTML("""
                        <div style="text-align: center; color: #cccccc; padding: 50px;">
                            <h2 style="color: #ff8a00;">TAB 4</h2>
                            <p>Content coming soon...</p>
                        </div>
                    """)
        
        # Event handlers
        
        # Text input events

        # Tab 3 Event handlers
        send_btn_tab3.click(
            handle_text_input_tab3,
            inputs=[msg_input_tab3, chatbot_tab3],
            outputs=[chatbot_tab3, msg_input_tab3]
        )

        msg_input_tab3.submit(
            handle_text_input_tab3,
            inputs=[msg_input_tab3, chatbot_tab3],
            outputs=[chatbot_tab3, msg_input_tab3]
        )

        # File upload event for Tab 3
        process_file_btn_tab3.click(
            handle_file_upload_tab3,
            inputs=[file_upload_tab3],
            outputs=[status_display_tab3]
        )

        # Voice input events for Tab 3
        process_voice_btn_tab3.click(
            handle_voice_input_tab3,
            inputs=[audio_input_tab3, chatbot_tab3, voice_chat_mode_tab3],
            outputs=[chatbot_tab3, audio_output_tab3, status_display_tab3]
        )

        # Voice reply event for Tab 3
        voice_reply_btn_tab3.click(
            handle_voice_reply_tab3,
            inputs=[chatbot_tab3, voice_chat_mode_tab3],
            outputs=[audio_output_tab3]
        )

        # Clear chat event for Tab 3
        clear_btn_tab3.click(
            handle_clear_tab3,
            outputs=[chatbot_tab3, msg_input_tab3]
        )




        send_btn.click(
            handle_text_input,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        msg_input.submit(
            handle_text_input,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        # File upload event
        process_file_btn.click(
            handle_file_upload,
            inputs=[file_upload],
            outputs=[status_display]
        )
        
        # Voice input events
        process_voice_btn.click(
            handle_voice_input,
            inputs=[audio_input, chatbot, voice_chat_mode],
            outputs=[chatbot, audio_output, status_display]
        )
        
        # Voice reply event
        voice_reply_btn.click(
            handle_voice_reply,
            inputs=[chatbot, voice_chat_mode],
            outputs=[audio_output]
        )
        
        # Clear chat event
        clear_btn.click(
            handle_clear,
            outputs=[chatbot, msg_input]
        )

        send_btn_tab2.click(
            handle_text_input_tab2,
            inputs=[msg_input_tab2, chatbot_tab2],
            outputs=[chatbot_tab2, msg_input_tab2]
        )
        
        msg_input_tab2.submit(
            handle_text_input_tab2,
            inputs=[msg_input_tab2, chatbot_tab2],
            outputs=[chatbot_tab2, msg_input_tab2]
        )
        
        # File upload event for Tab 2
        process_file_btn_tab2.click(
            handle_file_upload_tab2,
            inputs=[file_upload_tab2],
            outputs=[status_display_tab2]
        )
        
        # Voice input events for Tab 2
        process_voice_btn_tab2.click(
            handle_voice_input_tab2,
            inputs=[audio_input_tab2, chatbot_tab2, voice_chat_mode_tab2],
            outputs=[chatbot_tab2, audio_output_tab2, status_display_tab2]
        )
        
        # Voice reply event for Tab 2
        voice_reply_btn_tab2.click(
            handle_voice_reply_tab2,
            inputs=[chatbot_tab2, voice_chat_mode_tab2],
            outputs=[audio_output_tab2]
        )
        
        # Clear chat event for Tab 2
        clear_btn_tab2.click(
            handle_clear_tab2,
            outputs=[chatbot_tab2, msg_input_tab2]
        )
    
    return interface

# Main execution
if __name__ == "__main__":
    print("🎤 Starting FINBUZZ.AI Voice & Chat Financial Advisor (Gemini-Powered)...")
    print("📁 Loading GEMINI_API_KEY from .env file...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found! Please create a .env file with your GEMINI_API_KEY")
        exit(1)
    
    # Check if API key is loaded
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in .env file!")
        print("📝 Please add the following line to your .env file:")
        print("   GEMINI_API_KEY=your_actual_api_key_here")
        exit(1)
    
    print("✅ API key loaded successfully!")
    print("🎤 Loading Whisper medium model...")
    print("🚀 Launching Gradio interface...")
    
    # Create and launch the interface
    interface = create_gradio_interface()
    
    if interface is None:
        print("❌ Failed to create interface. Check your API key configuration.")
        exit(1)
    
    # Launch with custom settings
    interface.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,       # Custom port
        share=False,            # Set to True if you want a public link
        debug=True,             # Enable debug mode
        show_error=True,        # Show errors in UI
        inbrowser=True,         # Auto-open in browser
        favicon_path=None,      # You can add a custom favicon
        app_kwargs={
            "title": "FINBUZZ.AI - Voice & Chat Financial Advisor"
        }
    )