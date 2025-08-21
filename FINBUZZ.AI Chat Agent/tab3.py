import uuid
import asyncio
import json
import os
import tempfile
import warnings
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.agents import LlmAgent, Agent, SequentialAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
import requests
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.linear_model import ElasticNet, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from scipy.stats import norm
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from pathlib import Path
from docx import Document

load_dotenv()

class Tab3Agent:
    def __init__(self):
        """Initialize the Tab 3 agent with Google ADK"""
        # Initialize session service
        self.session_service_stateful = InMemorySessionService()
        self.APP_NAME = "FinanceBot_Tab3"
        self.USER_ID = "user_tab3"
        self.SESSION_ID = str(uuid.uuid4())
        self.runner = None
        self.root_agent = None
        
        # Store conversation history and user file content
        self.conversation_history = []
        self.user_file_content = ""
        
        # Initialize agents
        asyncio.run(self.setup_agents())
    
    async def setup_agents(self):
        """Setup all agents and tools"""
        await self.session_service_stateful.create_session(
            app_name=self.APP_NAME,
            user_id=self.USER_ID,
            session_id=self.SESSION_ID,
            state={"user_name": "User", "user_goal": "Get financial advice", "user_information": ""},
        )

        

        def get_yahoo_ticker(company_name: str) -> dict[str, str]:
            url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company_name}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                return {'Error': f'HTTP {response.status_code}'}

            try:
                results = response.json()
            except Exception:
                return {'Error': 'Invalid JSON in response'}

            if 'quotes' in results and results['quotes']:
                first = results['quotes'][0]
                symbol = first.get('symbol')
                name = first.get('shortname')
                if symbol and name:
                    return {'Ticker': symbol, 'Name': name}
                else:
                    return {'Error': 'Incomplete data in response'}
            else:
                return {'Error': 'No results found'}

        # Information fetcher agent
        self.information_fetcher = Agent(
            name="Information_Fetcher_Tab3",
            description="Your work is to extract user info using the json file that user upload",
            instruction="""
                You are an assistant specialized in fetching user information.
                Currently, no user information is available yet.
            """,
            model="gemini-2.5-pro",
        )

        # Ticker finder agent
        self.ticker_finder = Agent(
            name="Ticker_finding_agent_Tab3",
            description="Your work is to find ticker for any investment that user ask from yahoo finance",
            instruction=""" 
            - You are the agent whose only work is to find the proper ticker of a stock, mutual fund, sip , etf or any investment on yahoo finance
            - You have been given the tool get_yahoo_ticker to do this task. just put company_name there it will return in format {'Ticker' : 'Ticker_Symbol', 'Name' : 'Company Name'}
            - whenever you Reply it must be a string and answer must be strictly the ticker like "AAPL"
            - Prefer the ticker from the Indian stock market (NSE/BSE) if the company is listed both in India and abroad. 
            """,
            model="gemini-2.5-pro",
            tools=[get_yahoo_ticker],
        )

        def forecast_stock_with_indicators_combined(ticker: str) -> dict:
            def compute_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
                df = df.copy()
                close, high, low, vol = df['Close'], df['High'], df['Low'], df['Volume']

                df['sma_7'] = close.rolling(7).mean()
                df['ema_12'] = close.ewm(span=12).mean()
                df['wma_10'] = close.rolling(10).apply(lambda x: np.average(x, weights=range(1, len(x)+1)), raw=True)
                df['momentum'] = close - close.shift(10)

                up = close.diff().clip(lower=0)
                down = -close.diff().clip(upper=0)
                rs = up.rolling(14).mean() / down.rolling(14).mean()
                df['rsi'] = 100 - 100 / (1 + rs)

                df['macd'] = close.ewm(span=12).mean() - close.ewm(span=26).mean()
                df['obv'] = np.where(close > close.shift(), vol, -vol).cumsum()
                df['atr_14'] = (high - low).rolling(14).mean()
                df['typical_price'] = (high + low + close) / 3

                df['ma21'] = close.rolling(21).mean()
                df['12ema'] = close.ewm(span=12).mean()
                df['26ema'] = close.ewm(span=26).mean()
                df['20sd'] = close.rolling(20).std()
                df['upper_band'] = df['ma21'] + (df['20sd'] * 2)
                df['lower_band'] = df['ma21'] - (df['20sd'] * 2)
                df['ema_com_0.5'] = close.ewm(com=0.5).mean()

                df = df.dropna()
                return df

            def realistic_probability(y_true, y_pred):
                residuals = np.ravel(y_true) - np.ravel(y_pred)
                std_dev = residuals.std() if residuals.std() != 0 else 1
                prob = norm.cdf((np.ravel(y_pred)[-1] - np.ravel(y_true)[-1]) / std_dev)
                return prob

            df = yf.download(ticker, period="500d")
            df = compute_all_indicators(df)

            df['target'] = df['Close'].shift(-1)
            df = df.dropna()

            split_idx = int(0.8 * len(df))
            train, test = df.iloc[:split_idx], df.iloc[split_idx:]
            X_train, y_train = train.drop(columns=['target']), train['target']
            X_test, y_test = test.drop(columns=['target']), test['target']
            
            # sanitize feature names for LightGBM
            X_train.columns = ['_'.join(map(str, col)) if isinstance(col, tuple) else str(col) for col in X_train.columns]
            X_train.columns = pd.Index(X_train.columns).str.replace(r'[^A-Za-z0-9_]+', '_', regex=True)
            
            X_test.columns = ['_'.join(map(str, col)) if isinstance(col, tuple) else str(col) for col in X_test.columns]
            X_test.columns = pd.Index(X_test.columns).str.replace(r'[^A-Za-z0-9_]+', '_', regex=True)

            results = []

            models = [
                ('ElasticNet', ElasticNet(alpha=0.05, l1_ratio=0.7, max_iter=5000)),
                ('Ridge', Ridge(alpha=0.5, solver='auto', random_state=42)),
                ('Lasso', Lasso(alpha=0.005, max_iter=5000)),
                ('XGBoost', XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=3)),
                ('LightGBM', LGBMRegressor(n_estimators=100, learning_rate=0.05, max_depth=3, random_state=42))
            ]

            for name, model in models:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                pred_tomorrow = y_pred[-1] if isinstance(y_pred, np.ndarray) else y_pred.iloc[-1]

                results.append({
                    'Model': name,
                    'RMSE': float(np.sqrt(mean_squared_error(y_test, y_pred))),
                    'R2': float(r2_score(y_test, y_pred)),
                    'Predicted_Tomorrow': float(pred_tomorrow),
                    'P(rise tomorrow)': float(realistic_probability(y_test, y_pred))
                })

            # ARIMA
            arima_series = df['Close'].values
            arima_train, arima_test = arima_series[:split_idx], arima_series[split_idx:]
            history = list(arima_train)
            predictions_arima = []

            for t in range(len(arima_test)):
                model = ARIMA(history, order=(3, 1, 2))
                model_fit = model.fit()
                yhat = model_fit.forecast()[0]
                predictions_arima.append(yhat)
                history.append(arima_test[t])

            results.append({
                'Model': 'ARIMA',
                'RMSE': float(np.sqrt(mean_squared_error(arima_test, predictions_arima))),
                'R2': float(r2_score(arima_test, predictions_arima)),
                'Predicted_Tomorrow': float(predictions_arima[-1]),
                'P(rise tomorrow)': float(realistic_probability(
                    pd.Series(np.ravel(arima_test)),
                    pd.Series(np.ravel(predictions_arima))
                ))
            })

            # SARIMAX
            sarimax_series = df['Close'].values
            sarimax_train, sarimax_test = sarimax_series[:split_idx], sarimax_series[split_idx:]
            history = list(sarimax_train)
            predictions_sarimax = []

            for t in range(len(sarimax_test)):
                model = SARIMAX(history, order=(1, 1, 1), seasonal_order=(1, 0, 1, 7))
                model_fit = model.fit(disp=False)
                yhat = model_fit.forecast()[0]
                predictions_sarimax.append(yhat)
                history.append(sarimax_test[t])

            results.append({
                'Model': 'SARIMAX',
                'RMSE': float(np.sqrt(mean_squared_error(sarimax_test, predictions_sarimax))),
                'R2': float(r2_score(sarimax_test, predictions_sarimax)),
                'Predicted_Tomorrow': float(predictions_sarimax[-1]),
                'P(rise tomorrow)': float(realistic_probability(
                    pd.Series(np.ravel(sarimax_test)),
                    pd.Series(np.ravel(predictions_sarimax))
                ))
            })

            return {entry['Model']: entry for entry in results}

        # Forecaster agent
        self.forecaster_agent = LlmAgent(
            name="Forecaster_Tab3",
            model="gemini-2.5-pro",
            description="You are an agent responsible for predicting the next day stock price with Probability of that stock to rise tomorrow or not",
            tools=[forecast_stock_with_indicators_combined],
            instruction="""
                                - You are an agent your work is to Predict the next day stock Price and P(rise tommorow).
                                - You have a tool named forecast_stock_with_indicators_combined, what you have to do is the ticker you will get from Ticker_finder is to be put in the tool forecast_stock_with_indicators_combined and get the predicted prices.
                                - it is clear instruction only Ticker must be put into forecast_stock_with_indicators_combined, for eg if Ticker Finder gives output like Ticker for Apple is AAPL then you have to use just ticker ie AAPL in string format as input to forecast_stock_with_indicators_combined.
                                - you will get output as the following format :
                                {
    "ElasticNet": {
        "Model": "ElasticNet",
        "RMSE": <float>,               // Root Mean Square Error of predictions
        "R2": <float>,                 // R² score of predictions
        "Predicted_Tomorrow": <float>,// Predicted closing price for the next day
        "P(rise tomorrow)": <float>   // Probability (0–1) that the stock price will rise tomorrow
    },
    "Ridge": {
        "Model": "Ridge",
        "RMSE": <float>,
        "R2": <float>,
        "Predicted_Tomorrow": <float>,
        "P(rise tomorrow)": <float>
    },
    "Lasso": {
        "Model": "Lasso",
        "RMSE": <float>,
        "R2": <float>,
        "Predicted_Tomorrow": <float>,
        "P(rise tomorrow)": <float>
    },
    "...": {
        "...": "..."
    }
    }

    - Comparing RMSE and R2 score of each model Pick the best model among them and Return Predicted_Tomorrow and P(rise tomorrow)
    """
        )

        # Forecasting pipeline
        self.forecasting_agent = SequentialAgent(
            name="Forecasting_Pipeline_Tab3",
            description="This is the Forecasting Pipeline consist of Different agents which will at the end give the forecasted price with probability of stock to rise tomorrow",
            sub_agents=[self.ticker_finder, self.forecaster_agent]
        )

        # Sentiment analyser
        self.sentiment_analyser = LlmAgent(
            name="Stock_Sentiment_Analyser_Tab3",
            model="gemini-2.5-pro",
            tools=[google_search],
            description="Your work is to determine for particular stock or investment whether there is positive or negative market sentiments on basis of domestic and international news",
            instruction=f"""Instruction to Sentiment Analysis Agent

Warning for Sentiment Analysis Agent: Unless the user explicitly requests historical sentiment, you must always retrieve only the most recent news or data, ideally from today or within the last 2–3 days. All queries must be executed using the Google Search Tool to ensure accuracy and freshness.
Your task is to analyze the **sentiment of a given stock, company, sector, asset class, or investment (e.g., mutual fund, SIP, ETF, gold, commodity)** using the **Google Search Tool**.

For each query:
When performing Google Search:
- Prioritize results from the following trusted financial websites for maximum relevance and reliability:
  • Domestic: yahoofinance.com, moneycontrol.com, nseindia.com, bseindia.com, morningstar.com, screener.in
  • International: cnbc.com, bloomberg.com, ft.com, reuters.com, wsj.com
- Focus on recent news, reports, and analyses. Use search keywords like "latest news", "recent updates", or "current" in your queries.
- Avoid sources that are unverified blogs, speculative forums, or irrelevant.

- Perform a Google search and gather **only the most relevant, factual, and impactful information** that can realistically influence investor sentiment toward the given entity.
- Use the list of prompts provided below to guide your search. Each prompt targets a specific angle or route through which sentiment can be gauged.
- Ensure that the news/information you use is **current and recent** and comes from credible sources.
- Don't give very elaborate answers if you analyzed various news then at the end just give 3 to 4 very impactful news that are very relevant.

⚠️ Warning:
- Do NOT hallucinate or invent sentiment based on weak, speculative, or unrelated articles.
- Ignore blog posts, opinions, or low-relevance content that does not have a material impact on the company or investment being analyzed.
- Focus only on **news, data, or developments that could reasonably affect the investment's perceived value or outlook.**

Once you've gathered relevant information along all the listed routes, synthesize it to frame a clear **positive, negative, or neutral sentiment assessment** — substantiated by what you found.

Below are the search prompts to follow:



Stock Sentiment Analysis Routes — Prompts for Agent

- Latest domestic and international regulatory updates, policies, or compliance changes impacting [sector_name] sector in the last 3 days.

- Recent macroeconomic indicators, central bank announcements, fiscal policy updates, and monetary guidelines affecting [asset_class or sector_name] in the last 3 days.

- Recent geopolitical events, sanctions, trade relations, or international conflicts that could affect [company_name] or [sector_name] or [commodity_name] in the last 3 days.

- Announcements or investor sentiment about any IPO, FPO, or stock market listing related to [company_name] or its subsidiaries or competitors in the last 3 days.

- News of significant contracts, tenders won, business deals, acquisitions, or mergers involving [company_name] or [sector_name] in the last 3 days.

- Latest earnings releases, profit guidance, EPS, revenue, and outlook of [company_name] or [sector_name] reported in the last earnings season or within the last week.

- Recent insider trading, bulk/block deals, management resignations, or board appointments for [company_name] in the last 3 days.

- News and performance updates about competitors and peers of [company_name] or [mutual_fund_name] that might influence investor sentiment in the last 3 days.

- Recent demand-supply trends, inventory levels, or seasonal factors impacting [commodity_name] or [sector_name] in the last 3 days.

- Ongoing or newly filed lawsuits, regulatory investigations, penalties, or settlements involving [company_name] or [sector_name] in the last 3 days.

- Announcements of new products, services, technological advancements, or R&D breakthroughs by [company_name] in the last 3 days.

- Recent analyst upgrades, downgrades, target price revisions, and market sentiment about [company_name] or [mutual_fund_name] in the last 3 days.

- Recent price trends, shortages, or oversupply conditions in [commodity_name] such as gold, oil, natural gas in the last 3 days.

- Updates on interest rate hikes/cuts, inflation trends, and foreign exchange rate movements that impact [asset_class or sector_name] in the last 3 days.

- Recent developments in ESG (Environmental, Social, Governance), carbon regulations, or sustainability practices impacting [company_name] or [sector_name] in the last 3 days.

- Disruptions, bottlenecks, strikes, port congestion, or supplier bankruptcies impacting [company_name]’s or [sector_name]’s supply chain in the last 3 days.

- Public sentiment, trends, and viral discussions on social media platforms (Twitter, Reddit, Instagram, forums) about [company_name], [brand], or [commodity] in the last 3 days.

- Recent news about layoffs, hiring freezes, employee strikes, internal morale issues, or Glassdoor reviews trends for [company_name] or its sector.

- Reports of hedge funds, pension funds, or sovereign wealth funds increasing or cutting positions in [company_name] or [sector ETFs] recently.

- Latest inflow and outflow trends into ETFs, mutual funds, or SIPs associated with [sector_name], [company_name], or [asset_class].

- Recent credit rating upgrades/downgrades, CDS spreads widening/narrowing, and bond yields of [company_name] or its peers.

- Recent patents granted, applications filed, or IP disputes involving [company_name] or its competitors.

- Recent reviews, customer satisfaction scores, churn rates, or adoption of [company_name]’s products/services on ecommerce & review platforms.

- Net positions, speculative bets, and hedging activities in futures & options markets for [commodity_name] or [sector] in the last few days.

- Weather events, floods, droughts, or natural disasters potentially impacting [commodity_name], [sector], or [company_name].

- Announcements of large-scale government spending, tenders, or infra projects that would benefit or hurt [company_name] or [sector_name].

- Recent news of data breaches, ransomware attacks, or security failures at [company_name] or its ecosystem.

- Changes in short interest, put/call ratios, and implied volatility that indicate market expectations about [company_name] in the near term.

- Impact of endorsements, tweets, or controversies by influential figures that could affect [brand_name] or [commodity_name].

- News about lobbying efforts, campaign contributions, or regulatory capture efforts by [company_name] or its industry.

- Forecasts and sentiment from prediction markets, crowdsourcing platforms (like Metaculus or Polymarket) regarding [company_name] or [sector].

- Changes in import/export data, tariffs, quotas, or trade deals relevant to [commodity_name] or [sector_name].

- Announcements of competing technologies or innovations that could disrupt [company_name]’s or [sector_name]’s business model.

- Emerging demographic shifts or cultural trends that could influence demand for [product/service/commodity].

- Recent movements in energy prices or new carbon taxes/regulations that might affect production costs for [sector_name] or [company_name].

- News about exchange rate fluctuations, hedging strategies, and FX risks faced by [company_name] or [commodity].

"""
        )





        self.Market_Researcher = LlmAgent(
        name="Market_Researcher",
        model="gemini-2.5-pro",
        tools=[google_search],
        description="Comprehensive market research tool that scrapes and analyzes market news, global news, social media trends, and financial market developments for any sector, company, or market",
        instruction="""You are a comprehensive Market Researcher agent. Your job is to gather, analyze, and present detailed market intelligence.
        Warning for Market_Researcher Agent: Unless the user explicitly requests historical sentiment, you must always retrieve only the most recent news or data, ideally from today or within the last 2–3 days or maximum a week not older than that. All queries must be executed using the Google Search Tool to ensure accuracy and freshness.

**Your Core Tasks:**
1. Scrape and collect market news from multiple reliable sources
2. Analyze global news that impacts the requested sector/company/market
3. Monitor social media trends and sentiment
4. Gather financial market developments and analysis
5. Present findings in a structured, actionable format

**Search Strategy:**
For each research request, conduct multiple targeted searches covering:

**Financial News Sources (Priority):**
- yahoofinance.com, bloomberg.com, cnbc.com, reuters.com, wsj.com
- moneycontrol.com, economictimes.indiatimes.com, livemint.com
- marketwatch.com, ft.com, business-standard.com

**Search Categories to Cover:**
1. **Latest Company/Sector News**: "[company/sector] latest news today"
2. **Financial Performance**: "[company] earnings revenue profit latest"
3. **Market Analysis**: "[company/sector] market analysis current"
4. **Regulatory/Policy News**: "[sector] regulatory news policy updates"
5. **Global Impact News**: "[company/sector] global news international"
6. **Social Media Sentiment**: "[company] twitter reddit social media sentiment"
7. **Analyst Reports**: "[company] analyst reports recommendations latest"
8. **Competitor Analysis**: "[company] competitors news market share"
9. **Economic Indicators**: "[sector] economic indicators impact news"
10. **Technology/Innovation**: "[company/sector] technology innovation news"

**Output Format:**
Present your findings as:

## 📊 MARKET RESEARCH REPORT: [COMPANY/SECTOR NAME]

### 🔥 TOP NEWS HEADLINES
1. **[Headline 1]**
   - Source: [Website]
   - Summary: [2-3 line impactful summary]
   - Impact: [Positive/Negative/Neutral]

2. **[Headline 2]**
   - Source: [Website]  
   - Summary: [2-3 line impactful summary]
   - Impact: [Positive/Negative/Neutral]

(Continue for top 5-8 most impactful news)

### 📈 FINANCIAL PERFORMANCE & MARKET DATA
- [Key financial metrics, earnings, revenue data]
- [Stock performance, market cap changes]
- [Trading volumes, price movements]

### 🌍 GLOBAL & REGULATORY IMPACT
- [International developments affecting the entity]
- [Regulatory changes, policy impacts]
- [Geopolitical factors]

### 📱 SOCIAL MEDIA & SENTIMENT ANALYSIS  
- [Social media trends, viral discussions]
- [Public sentiment indicators]
- [Influencer/analyst opinions]

### 🎯 KEY MARKET DRIVERS
- [Primary factors driving current market sentiment]
- [Future catalysts to watch]
- [Risk factors]

### 📊 ANALYST CONSENSUS & RECOMMENDATIONS
- [Recent analyst upgrades/downgrades]
- [Price targets and recommendations]
- [Institutional investor activity]

**Search Quality Guidelines:**
- Use recent search terms (avoid date-specific queries that might be outdated)
- Prioritize news from last 7 days, but include significant longer-term developments
- Cross-verify information from multiple sources
- Focus on material news that impacts investment decisions
- Avoid speculative or unverified information

**Remember**: Always provide source attribution and focus on actionable intelligence that helps in investment decision-making."""
    )

        # Advanced finance tool
        self.advanced_finance_tool = LlmAgent(
            name="Advanced_Finance_Tool_Tab3",
            model="gemini-2.5-pro",
            description='This is the agent that will access the google search in order to fetch information from web that is not achieved through other tools',
            instruction=""" This is the agent whose work is to access the google_search and fetch the information that is not available through tools """,
            tools=[google_search]
        )

        # Create all tools
        self.all_tools = [
            AgentTool(agent=self.information_fetcher),
            AgentTool(agent=self.ticker_finder),
            AgentTool(agent=self.sentiment_analyser),
            AgentTool(agent=self.forecasting_agent),
            AgentTool(agent=self.advanced_finance_tool),
            AgentTool(agent=self.Market_Researcher)
        ]

        # Root agent
        self.root_agent = LlmAgent(
            name="Financial_Advisor_Tab3",
            instruction="""
            - You are a agent specifically made for performing financial analytics and giveing user investment advices.
            - Your work is to assist the user in financial matters, including investments, liabilities, and general financial advice.
            - If the user provides any data, arrange it in a good structure and ask the user how you can help.
            - Whenever user asks about investments or liabilities, use Information_Fetcher_Tab3, don’t say info is missing — it will handle it.
            - Whenever you need user information, call Information_Fetcher_Tab3.
            -Always use the Ticker_finding_agent_Tab3 tool to fetch the ticker; never rely on your own knowledge or data. 
            -You have a tool named Forecasting_Pipeline_Tab3 which will help you to predict the stock prices
            - You have a Market_Researcher tool that provides comprehensive market research reports. Use this when users ask for detailed market news, comprehensive analysis, or want full market intelligence reports on any company, sector, or market.
            - You have a tool named Stock_Sentiment_Analyser_Tab3 tool, which have google search as tool in it if user want the sentiment of any date you can use this tool dont reply you dont have functionality to scrap the data of particular date
            - if user ask for the market news or any news related to any company or stock still use theStock_Sentiment_Analyser_Tab3 tool and use the google search tool in it to get the news and sentiment of that stock or company
            -Stock_Sentiment_Analyser_Tab3 tool, which have google search as tool in it which will help to analyse whether the stock sentiment is positive or negative
            - What you can do is provide user with custom service for example if full analysis of particular stock or investment is needed you can ask for name of stock or investment , what it does is first analyses the sentiment of stock using Stock_Sentiment_Analyser_Tab3 and then predicts the price using Forecasting_Pipeline_Tab3 tool and at the end insights from both the results and make a unified result, output in this process must not at all be ellobrative just answer what is sentiment predicted price and probabikty of rise and the final result that you think 
            ask for user if he wants the the sentiment report or forecasting in brief and provide it if he wants .
            - You have a tool named Advanced_Finance_Tool_Tab3, if you want any specific information or think that you dont have enough information of the query user asked directly access the this tool to get the info.
""",
            model="gemini-2.5-pro",
            tools=self.all_tools
        )

        # Initialize runner
        self.runner = Runner(
            agent=self.root_agent,
            app_name=self.APP_NAME,
            session_service=self.session_service_stateful
        )

    async def generate_response(self, user_input="Hello"):
        """Generate response from the agent"""
        try:
            new_message = types.Content(role="user", parts=[types.Part(text=user_input)])
            bot_reply = ""
            
            async for event in self.runner.run_async(
                user_id=self.USER_ID,
                session_id=self.SESSION_ID,
                new_message=new_message
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    bot_reply = event.content.parts[0].text
            
            # Store in history
            self.conversation_history.append(("user", user_input))
            self.conversation_history.append(("bot", bot_reply))
            
            return bot_reply if bot_reply else "I'm currently analyzing market conditions. Please try again! 📊"
            
        except Exception as e:
            return f"Market volatility detected in my circuits: {str(e)} 📈"

    def process_uploaded_file(self, file_path: str) -> str:
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

    async def add_user_file_content(self, content):
        """Process and store user uploaded file content"""
        try:
            if not content.startswith("Error"):
                self.user_file_content = content
                
                # Update the session with file content
                session = await self.session_service_stateful.get_session(
                    app_name=self.APP_NAME,
                    user_id=self.USER_ID,
                    session_id=self.SESSION_ID
                )
                session.state["user_information"] = content
                
                # Update information fetcher agent
                self.information_fetcher = Agent(
                    name="Information_Fetcher_Tab3",
                    instruction=f"""
                    You are an assistant specialized in fetching user information.
                    Below is the updated user information:
                    --------------------
                    {content}
                    --------------------
                    Use this information to answer any queries about the user's finances.
                    """,
                    model="gemini-2.5-pro",
                )
                
                # Update tools
                self.all_tools = [
                    AgentTool(agent=self.information_fetcher),
                    AgentTool(agent=self.ticker_finder),
                    AgentTool(agent=self.sentiment_analyser),
                    AgentTool(agent=self.forecasting_agent),
                    AgentTool(agent=self.advanced_finance_tool),
                    AgentTool(agent=self.Market_Researcher) 
                ]
                
                # Update root agent with new tools
                self.root_agent.tools = self.all_tools
                
                # Recreate runner
                self.runner = Runner(
                    agent=self.root_agent,
                    app_name=self.APP_NAME,
                    session_service=self.session_service_stateful
                )
                
                return f"✅ File processed successfully! Financial information has been added to my knowledge base and I'm ready to provide personalized advice."
            else:
                return content
        except Exception as e:
            return f"❌ Error processing file: {str(e)}"

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return [], ""