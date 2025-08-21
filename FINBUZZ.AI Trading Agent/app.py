# app.py
from __future__ import annotations
import time
import threading
import gradio as gr
import pandas as pd
from trader_agent import TraderAgent

agent = None
runner_thread = None
runner_stop = threading.Event()
runner_speed_sec = 60.0  # 60 seconds per bar for 1-minute mode
is_running = False

def launch_trader(starting_cash: float, ticker: str):
    if starting_cash is None or starting_cash <= 0:
        return gr.update(value="Starting cash must be > 0"), None, None, None, None
    if not ticker or "." not in ticker:
        return gr.update(value="Enter an NSE ticker like HUDCO.NS"), None, None, None, None
    global agent
    try:
        agent = TraderAgent()  # This creates the AI agent
        state = agent.initialize(ticker.strip(), float(starting_cash))
        return (
            gr.update(value=f"🤖 AI AGENT READY! CSV saved: {state['csv_path']}"),
            state["fig"],
            pd.DataFrame([state["portfolio"]]),
            "\n".join(state["logs"]),
            gr.update(visible=True)
        )
    except Exception as e:
        return (
            gr.update(value=f"❌ Error initializing AI agent: {str(e)}"),
            None, None, None, None
        )

def _loop_runner(speed_mode: str):
    """AI Agent continuous trading loop"""
    global agent, is_running, runner_stop, runner_speed_sec
    is_running = True
    step_count = 0
    
    try:
        while not runner_stop.is_set():
            step_count += 1
            if agent and agent.state:
                agent.state.log(f"🤖 AI Agent executing step {step_count}...")
            
            # Use the AI agent's step_once method
            step = agent.step_once()  # This is where AI agent makes trading decisions
            
            if step.get("done"):
                if agent and agent.state:
                    agent.state.log("✅ Trading session completed by AI Agent")
                break
                
            # Update speed based on mode
            sleep_time = 300 if speed_mode == "Real-time (5m)" else runner_speed_sec
            time.sleep(sleep_time)
            
    except Exception as e:
        if agent and agent.state:
            agent.state.log(f"❌ AI Agent error: {str(e)}")
    finally:
        is_running = False

def start_run(speed_mode: str):
    global runner_thread, runner_stop
    if agent is None:
        return gr.update(value="❌ Launch the AI agent first from Setup tab.")
    if is_running:
        return gr.update(value="🤖 AI Agent already running...")
    
    runner_stop.clear()
    t = threading.Thread(target=_loop_runner, args=(speed_mode,), daemon=True)
    t.start()
    return gr.update(value=f"🤖 AI AGENT STARTED in {speed_mode} mode...")

def pause_run():
    global runner_stop
    runner_stop.set()
    return gr.update(value="⏸️ AI Agent paused.")

def step_once():
    """Single step using AI agent"""
    if agent is None or agent.state is None:
        return None, None, "❌ AI Agent not initialized"
    
    try:
        # This calls the AI agent's decision making
        step = agent.step_once()  # AI agent makes BUY/SELL/HOLD decision here
        
        if step.get("done"):
            return agent.state.chart.to_json(), pd.DataFrame([agent.state.portfolio.snapshot()]), "✅ Trading completed"
        
        snap = agent.state.portfolio.snapshot()
        return agent.state.chart.to_json(), pd.DataFrame([snap]), "\n".join(agent.state.logs[-200:])
        
    except Exception as e:
        error_msg = f"❌ AI Agent step failed: {str(e)}"
        if agent and agent.state:
            agent.state.log(error_msg)
        return None, None, error_msg

def fetch_live_state():
    if agent is None or agent.state is None:
        return None, None, None
    snap = agent.state.portfolio.snapshot()
    return agent.state.chart.to_json(), pd.DataFrame([snap]), "\n".join(agent.state.logs[-200:])

def get_ai_analytics():
    """Get AI analytics without changing core logic"""
    if agent is None or agent.state is None:
        return None, None, None, None
    
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    # Get current portfolio data
    snap = agent.state.portfolio.snapshot()
    
    # Get trade history from portfolio
    trades = agent.state.portfolio.trade_log if hasattr(agent.state.portfolio, 'trade_log') else []
    
    # Create performance metrics
    total_trades = len(trades)
    buy_trades = [t for t in trades if t.side == "BUY"]
    sell_trades = [t for t in trades if t.side == "SELL"]
    
    # Calculate P&L over time
    pnl_history = []
    cumulative_pnl = 0
    timestamps = []
    
    for i, trade in enumerate(trades):
        if trade.side == "SELL" and i > 0:
            # Simple P&L calculation
            prev_buy = None
            for j in range(i-1, -1, -1):
                if trades[j].side == "BUY":
                    prev_buy = trades[j]
                    break
            if prev_buy:
                pnl = (trade.price - prev_buy.price) * trade.qty
                cumulative_pnl += pnl
        
        pnl_history.append(cumulative_pnl)
        timestamps.append(trade.ts)
    
    # Create analytics charts
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("📈 Cumulative P&L", "📊 Trade Distribution", "💰 Portfolio Value", "🎯 Win Rate"),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "indicator"}, {"type": "indicator"}]]
    )
    
    # P&L Chart
    if pnl_history and timestamps:
        fig.add_trace(
            go.Scatter(
                x=timestamps[-len(pnl_history):],
                y=pnl_history,
                mode='lines+markers',
                name='Cumulative P&L',
                line=dict(color='#00ff88', width=3),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
    
    # Trade Distribution
    fig.add_trace(
        go.Bar(
            x=['Buy Orders', 'Sell Orders'],
            y=[len(buy_trades), len(sell_trades)],
            marker_color=['#00ff88', '#ff4444'],
            name='Trade Count'
        ),
        row=1, col=2
    )
    
    # Portfolio Value Indicator
    fig.add_trace(
        go.Indicator(
            mode="number+gauge+delta",
            value=snap.get('cash', 0) + snap.get('shares', 0) * snap.get('last_price', 0),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Portfolio Value (₹)"},
            gauge={'axis': {'range': [0, snap.get('cash', 10000) * 2]},
                   'bar': {'color': "#00ff88"},
                   'bgcolor': "white",
                   'borderwidth': 2,
                   'bordercolor': "#00ff88"}
        ),
        row=2, col=1
    )
    
    # Win Rate Indicator
    profitable_trades = sum(1 for i, trade in enumerate(trades) 
                          if trade.side == "SELL" and i > 0 and 
                          any(t.side == "BUY" and t.price < trade.price for t in trades[:i]))
    win_rate = (profitable_trades / len(sell_trades) * 100) if sell_trades else 0
    
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=win_rate,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Win Rate (%)"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "#00ff88"},
                   'bgcolor': "white",
                   'borderwidth': 2,
                   'bordercolor': "#00ff88",
                   'threshold': {'line': {'color': "red", 'width': 4},
                               'thickness': 0.75, 'value': 50}}
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        template="plotly_dark",
        paper_bgcolor='#1a1a1a',
        plot_bgcolor='#1a1a1a',
        font=dict(color='white', family="JetBrains Mono")
    )
    
    # Create summary stats
    stats_data = {
        'Metric': ['Total Trades', 'Buy Orders', 'Sell Orders', 'Current P&L', 'Current Shares', 'Available Cash'],
        'Value': [total_trades, len(buy_trades), len(sell_trades), 
                 f"₹{snap.get('total_pnl', 0):.2f}", snap.get('shares', 0), 
                 f"₹{snap.get('cash', 0):.2f}"]
    }
    
    return fig, pd.DataFrame(stats_data), f"📊 Analytics Updated | Trades: {total_trades} | P&L: ₹{snap.get('total_pnl', 0):.2f}", snap.get('total_pnl', 0)

# Enhanced Premium CSS - Fixed font and removed green strips
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'JetBrains Mono', monospace !important;
}

body {
    background: #0a0a0a !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.gradio-container {
    background: #0a0a0a !important;
    color: #ffffff !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Main Header Styling */
.main-header {
    background: linear-gradient(135deg, #00ff88 0%, #00cc66 50%, #00d4ff 100%) !important;
    color: black !important;
    font-weight: 800 !important;
    font-size: 2.2rem !important;
    padding: 20px !important;
    border-radius: 15px !important;
    text-align: center !important;
    box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3) !important;
    margin-bottom: 20px !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.sub-header {
    background: #1a1a1a !important;
    color: #00ff88 !important;
    padding: 10px 15px !important;
    border-radius: 10px !important;
    text-align: center !important;
    font-weight: 600 !important;
    margin-bottom: 25px !important;
    border: 2px solid #333333 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Premium Button Styles */
.premium-btn {
    background: linear-gradient(135deg, #00ff88 0%, #00cc66 100%) !important;
    border: none !important;
    color: black !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    padding: 12px 24px !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 15px rgba(0, 255, 136, 0.4) !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.premium-btn:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(0, 255, 136, 0.6) !important;
    background: linear-gradient(135deg, #00cc66 0%, #00ff88 100%) !important;
}

.secondary-btn {
    background: linear-gradient(135deg, #00d4ff 0%, #8b5cf6 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Input Field Styling - Removed green strips */
.input-field input, .input-field textarea {
    background: #1a1a1a !important;
    border: 2px solid #333333 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    padding: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    transition: border-color 0.3s ease !important;
}

.input-field input:focus, .input-field textarea:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 10px rgba(0, 255, 136, 0.3) !important;
}

/* Status Box Styling - Removed green strips */
.status-box textarea {
    background: #1a1a1a !important;
    color: #ffffff !important;
    border: 2px solid #333333 !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
}

/* Chart Container */
.chart-container {
    background: #1a1a1a !important;
    border: 2px solid #333333 !important;
    border-radius: 15px !important;
    padding: 10px !important;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5) !important;
}

/* DataFrames - Removed green strips */
.dataframe {
    background: #1a1a1a !important;
    border: 2px solid #333333 !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.dataframe th {
    background: #333333 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.dataframe td {
    color: #ffffff !important;
    border-bottom: 1px solid #333333 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Logs Styling - Removed green strips */
.logs-container textarea {
    background: #0a0a0a !important;
    color: #ffffff !important;
    border: 2px solid #333333 !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    line-height: 1.4 !important;
}

/* Tab Styling */
.tab-nav button {
    background: #2a2a2a !important;
    color: #cccccc !important;
    border: 1px solid #333333 !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.tab-nav button.selected {
    background: #00ff88 !important;
    color: black !important;
    border-color: #00ff88 !important;
}

/* Analytics Cards - Removed green strips */
.analytics-card {
    background: #1a1a1a !important;
    border: 2px solid #333333 !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin: 10px !important;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Accordion Styling */
.accordion {
    background: #1a1a1a !important;
    border: 2px solid #333333 !important;
    border-radius: 10px !important;
}

.accordion summary {
    background: #2a2a2a !important;
    color: #ffffff !important;
    padding: 15px !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Radio Button Styling */
.radio-group label {
    background: #2a2a2a !important;
    color: #ffffff !important;
    border: 2px solid #333333 !important;
    border-radius: 8px !important;
    padding: 10px 15px !important;
    margin: 5px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.radio-group label:hover {
    border-color: #00ff88 !important;
    color: #00ff88 !important;
}

.radio-group input:checked + label {
    background: #00ff88 !important;
    color: black !important;
    border-color: #00ff88 !important;
}

/* Remove all green border strips */
textarea, input {
    border-left: none !important;
    border-right: none !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #1a1a1a;
}

::-webkit-scrollbar-thumb {
    background: #333333;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #00ff88;
}

/* Ensure all text uses JetBrains Mono */
h1, h2, h3, h4, h5, h6, p, span, div, label, button {
    font-family: 'JetBrains Mono', monospace !important;
}
"""

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as demo:
    # Main Header
    gr.Markdown("# 🤖 AI-POWERED AUTONOMOUS TRADING AGENT", elem_classes="main-header")
    gr.Markdown("### Intelligent Agent-Only Trading • 1-Minute Timeframe • Microsoft AutoGen", elem_classes="sub-header")

    with gr.Tab("🔧 Agent Setup"):
        with gr.Row():
            with gr.Column():
                cash = gr.Number(
                    label="💰 Starting Cash (₹)", 
                    value=10000, 
                    precision=0,
                    elem_classes="input-field"
                )
            with gr.Column():
                ticker = gr.Textbox(
                    label="📈 NSE Ticker (e.g., HUDCO.NS)", 
                    value="HUDCO.NS",
                    elem_classes="input-field"
                )
        
        launch_btn = gr.Button(
            "🚀 LAUNCH AI TRADING AGENT", 
            variant="primary", 
            elem_classes="premium-btn",
            size="lg"
        )
        
        status = gr.Textbox(
            label="🔄 AI Agent Status", 
            interactive=False,
            elem_classes="status-box"
        )
        
        chart_state = gr.State()
        
        with gr.Accordion("📋 AI Agent Instructions - Go to Trading tab after launch", open=True, elem_classes="accordion"):
            gr.Markdown("""
            **🎯 AI TRADING AGENT FEATURES:**
            - **Autonomous Decision Making:** AI agent analyzes market data and makes BUY/SELL/HOLD decisions
            - **Real-time 1-minute candlestick analysis** with technical indicators
            - **Intelligent position sizing** based on market conditions and performance
            - **Advanced risk management** with stop-losses and profit-taking
            - **Learning system** that adapts based on trading performance
            
            **⚡ SPEED MODES:**
            - **Fast (1min per bar):** Rapid simulation - 60 second intervals
            - **Real-time (5m):** Live market simulation - 5 minute intervals
            
            **🤖 AI AGENT REQUIREMENTS:**
            - Requires OpenAI API Key or Gemini API Key in .env file
            - Agent will use fallback deterministic strategy if no API key
            """, elem_classes="analytics-card")

        # Hidden element to toggle Tab 2 visibility
        tab2_visible = gr.Checkbox(visible=False)

        # Outputs for preview in Setup
        with gr.Row():
            with gr.Column(scale=2):
                preview_fig = gr.Plot(
                    label="📈 Market Context Preview - AI Agent Analysis", 
                    elem_classes="chart-container"
                )
            with gr.Column(scale=1):
                preview_port = gr.Dataframe(
                    label="💼 Portfolio Preview", 
                    interactive=False,
                    elem_classes="dataframe"
                )
                preview_logs = gr.Textbox(
                    label="📝 AI Agent Logs", 
                    interactive=False, 
                    lines=6,
                    elem_classes="logs-container"
                )

        launch_btn.click(
            launch_trader, inputs=[cash, ticker],
            outputs=[status, preview_fig, preview_port, preview_logs, tab2_visible]
        )

    with gr.Tab("🎯 AI Agent Trading"):
        with gr.Row():
            with gr.Column(scale=1):
                speed = gr.Radio(
                    ["Fast (1min per bar)", "Real-time (5m)"],
                    value="Fast (1min per bar)", 
                    label="⚡ AI Agent Speed",
                    elem_classes="radio-group"
                )
            with gr.Column(scale=2):
                with gr.Row():
                    start = gr.Button(
                        "🤖 START AI AGENT TRADING", 
                        variant="primary",
                        elem_classes="premium-btn",
                        size="lg"
                    )
                    pause = gr.Button(
                        "⏸️ PAUSE AI AGENT", 
                        elem_classes="secondary-btn"
                    )
                    step = gr.Button(
                        "⭐ AI AGENT SINGLE STEP", 
                        elem_classes="secondary-btn"
                    )
        
        # Main Trading Interface
        with gr.Row():
            with gr.Column(scale=3):
                fig = gr.Plot(
                    label="📊 AI Agent Live Trading - Premium Candlesticks + Trade Signals", 
                    elem_classes="chart-container"
                )
            with gr.Column(scale=1):
                port = gr.Dataframe(
                    label="💼 AI Portfolio Status", 
                    interactive=False,
                    elem_classes="dataframe"
                )
        
        logs = gr.Textbox(
            label="🤖 AI Agent Intelligence Logs - Real-time Decision Making", 
            interactive=False, 
            lines=16,
            elem_classes="logs-container"
        )

        # background polling to keep UI fresh
        poll = gr.Timer(1.0, active=True)
        poll.tick(fn=fetch_live_state, outputs=[fig, port, logs])

        # Event handlers - using AI agent methods
        start.click(start_run, inputs=[speed], outputs=[logs])
        pause.click(pause_run, outputs=[logs])
        step.click(step_once, outputs=[fig, port, logs])

    with gr.Tab("📊 AI Analytics"):
        gr.Markdown("### 🧠 AI Agent Performance Analytics", elem_classes="sub-header")
        
        with gr.Row():
            refresh_analytics_btn = gr.Button(
                "🔄 REFRESH AI ANALYTICS", 
                variant="primary",
                elem_classes="premium-btn",
                size="lg"
            )
            analytics_status = gr.Textbox(
                label="📊 Analytics Status",
                interactive=False,
                elem_classes="status-box"
            )
        
        with gr.Row():
            with gr.Column(scale=3):
                analytics_plot = gr.Plot(
                    label="📈 AI Agent Performance Dashboard - P&L, Trades, Win Rate & Portfolio Value",
                    elem_classes="chart-container"
                )
            with gr.Column(scale=1):
                stats_table = gr.Dataframe(
                    label="📋 AI Trading Statistics",
                    interactive=False,
                    elem_classes="dataframe"
                )
        
        # Performance Metrics Cards
        with gr.Row():
            with gr.Column():
                total_pnl_display = gr.Number(
                    label="💰 AI Agent Total P&L (₹)",
                    interactive=False,
                    elem_classes="input-field"
                )
            with gr.Column():
                gr.Markdown("""
                **🤖 AI AGENT PERFORMANCE METRICS:**
                - Real-time P&L tracking from AI decisions
                - Win/Loss ratio analysis of AI trades  
                - AI agent decision frequency analysis
                - Portfolio utilization by AI agent
                - Learning curve and adaptation metrics
                """, elem_classes="analytics-card")
        
        # Analytics event handlers
        refresh_analytics_btn.click(
            get_ai_analytics,
            outputs=[analytics_plot, stats_table, analytics_status, total_pnl_display]
        )
        
        # Auto-refresh analytics every 10 seconds
        analytics_timer = gr.Timer(10.0, active=True)
        analytics_timer.tick(
            fn=get_ai_analytics,
            outputs=[analytics_plot, stats_table, analytics_status, total_pnl_display]
        )

if __name__ == "__main__":
    demo.launch()