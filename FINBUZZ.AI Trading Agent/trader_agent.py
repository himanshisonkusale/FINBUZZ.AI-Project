from __future__ import annotations
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, List
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import asyncio
import json
import numpy as np

from market import download_and_prepare, StreamCursor
from portfolio import Portfolio
from charting import Candles

# --- Microsoft AutoGen imports
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


@dataclass
class TradingMemory:
    """Enhanced trading memory for learning and decision making"""
    trade_history: List[Dict] = field(default_factory=list)
    performance_metrics: Dict = field(default_factory=dict)
    market_patterns: List[Dict] = field(default_factory=list)
    
    def add_trade(self, trade_data: Dict):
        self.trade_history.append(trade_data)
        self.update_performance_metrics()
    
    def update_performance_metrics(self):
        if not self.trade_history:
            return
        
        total_trades = len(self.trade_history)
        profitable_trades = sum(1 for t in self.trade_history if t.get('pnl', 0) > 0)
        
        self.performance_metrics.update({
            'total_trades': total_trades,
            'win_rate': profitable_trades / total_trades if total_trades > 0 else 0,
            'avg_pnl': sum(t.get('pnl', 0) for t in self.trade_history) / total_trades if total_trades > 0 else 0,
            'best_trade': max((t.get('pnl', 0) for t in self.trade_history), default=0),
            'worst_trade': min((t.get('pnl', 0) for t in self.trade_history), default=0)
        })
    
    def get_recent_performance(self, last_n: int = 10) -> Dict:
        recent_trades = self.trade_history[-last_n:] if len(self.trade_history) >= last_n else self.trade_history
        if not recent_trades:
            return {}
        
        recent_pnl = [t.get('pnl', 0) for t in recent_trades]
        return {
            'recent_trades': len(recent_trades),
            'recent_avg_pnl': sum(recent_pnl) / len(recent_pnl),
            'recent_win_rate': sum(1 for pnl in recent_pnl if pnl > 0) / len(recent_pnl)
        }


@dataclass
class AppState:
    ticker: str
    data_df: pd.DataFrame
    csv_path: Path
    stream: StreamCursor
    chart: Candles = field(default_factory=Candles)
    portfolio: Portfolio = field(default_factory=lambda: Portfolio(cash=0.0))
    logs: List[str] = field(default_factory=list)
    trading_memory: TradingMemory = field(default_factory=TradingMemory)
    historical_data: List[Dict] = field(default_factory=list)  # Store historical bar data
    # NEW: Manual override flags
    manual_sell_all: bool = field(default=False)
    manual_buy_max: bool = field(default=False)
    last_manual_action: str = field(default="")

    def log(self, msg: str):
        self.logs.append(msg)
        print(msg)


def _make_intelligent_policy_prompt(ticker: str) -> str:
    return f"""
You are an AGGRESSIVE and INTELLIGENT intraday trading agent operating on 1-minute bars for {ticker}.

ENHANCED RULES (strict):
- You receive the current bar's Open and Volume while forming; Close is UNKNOWN until bar ends.
- You MUST make BUY/SELL/HOLD decisions BEFORE the bar ends. All fills occur at the known Open price.
- Start with 1-day context (no trades). First trade must be on first bar AFTER context day.
- Long-only strategy, integer shares only. Never short.
- AGGRESSIVE CAPITAL DEPLOYMENT: Use up to 90% of available cash for high-conviction trades
- INTELLIGENT RISK MANAGEMENT: Max 50% per single buy order, but can scale into positions
- LEARNING SYSTEM: You have access to complete trade history and performance metrics

ENHANCED TRADING INTELLIGENCE:
1. MOMENTUM & VOLUME ANALYSIS:
   - Strong buy signals: Open > EMA20, Volume > 2x average, positive price momentum
   - Scale into winners: If existing position profitable, add more on continued strength
   - Quick exits: Cut losses fast if momentum reverses (stop loss at -2% from entry)

2. PATTERN RECOGNITION:
   - Learn from your trading history - avoid repeating losing patterns
   - Identify your most profitable setups and trade them more aggressively  
   - Track which volume/price combinations work best for entries

3. POSITION SIZING STRATEGY:
   - High conviction (strong signals): Use 40-50% of available cash
   - Medium conviction: Use 25-35% of available cash
   - Low conviction/scalping: Use 10-20% of available cash
   - Scale out profits: Take partial profits on 2%+ gains, let winners run

4. ADAPTIVE LEARNING:
   - If win rate < 40%, become more selective with entries
   - If win rate > 60%, become more aggressive with position sizing
   - Track your best performing times of day and focus trading then

TOOL USAGE SEQUENCE (MANDATORY):
1. get_next_open_volume() - Get next bar data
2. get_trading_memory() - Review your trading history and performance
3. Analyze current market conditions with your historical context
4. Make informed trading decision based on signals + your learning
5. place_order() if trading (BUY/SELL with aggressive but smart sizing)  
6. on_bar_close() - Always call this to complete the bar

YOU MUST MAKE TRADING DECISIONS AND PLACE ORDERS. This is a LIVE trading system!
BE PROFITABLE, AGGRESSIVE, AND LEARN FROM EVERY TRADE. Your goal is to maximize returns while managing risk intelligently.
"""


class TraderAgent:
    def __init__(self, model_name: str = "gpt-4o-mini", use_llm: bool = True):
        self.use_llm = str(os.getenv("USE_LLM", "true")).lower() == "true" and use_llm
        
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY_TraderAgent")
        if not api_key:
            self.use_llm = False
            print("Warning: No API key found, using fallback trading logic")
        
        if self.use_llm and api_key:
            # Create model client - use Gemini if available
            if os.getenv("GEMINI_API_KEY_TraderAgent"):
                self.model_client = OpenAIChatCompletionClient(
                    model="gemini-2.0-flash",
                    api_key=os.getenv("GEMINI_API_KEY_TraderAgent"),
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                )
            else:
                self.model_client = OpenAIChatCompletionClient(
                    model=model_name,
                    api_key=api_key
                )
        
        self.agent: Optional[AssistantAgent] = None
        self.state: Optional[AppState] = None

    # ------------------------
    # Enhanced Tools for LLM
    # ------------------------
    def tool_portfolio_state(self) -> Dict[str, Any]:
        """Return current portfolio snapshot with enhanced metrics."""
        base_snapshot = self.state.portfolio.snapshot()
        
        # Add enhanced metrics
        if self.state.portfolio.last_price > 0:
            total_value = base_snapshot['cash'] + base_snapshot['shares'] * base_snapshot['last_price']
            base_snapshot['total_value'] = round(total_value, 2)
            base_snapshot['cash_utilization'] = round((1 - base_snapshot['cash'] / total_value) * 100, 2)
        
        return base_snapshot

    def tool_get_trading_memory(self) -> Dict[str, Any]:
        """Return trading history and performance metrics for learning."""
        memory = self.state.trading_memory
        return {
            'total_trades': len(memory.trade_history),
            'performance_metrics': memory.performance_metrics,
            'recent_performance': memory.get_recent_performance(10),
            'last_5_trades': memory.trade_history[-5:] if memory.trade_history else [],
            'historical_bars_count': len(self.state.historical_data)
        }

    def tool_place_order(self, side: str, qty: int, price: float, ts_iso: str) -> Dict[str, Any]:
        """Enhanced order placement with trade tracking."""
        if side.upper() == "BUY":
            res = self.state.portfolio.buy(ts_iso, qty, price)
            if res.get("ok"):
                self.state.chart.add_trade_marker(ts_iso, price, "BUY")
                self.state.log(f"🟢 AGENT BUY {qty} @ ₹{price} [{ts_iso}] - Position: {self.state.portfolio.shares}")
                
                # Track trade for learning
                trade_data = {
                    'timestamp': ts_iso,
                    'side': 'BUY',
                    'qty': qty,
                    'price': price,
                    'portfolio_value_before': self.state.portfolio.cash + qty * price
                }
                self.state.trading_memory.add_trade(trade_data)
        
        elif side.upper() == "SELL":
            res = self.state.portfolio.sell(ts_iso, qty, price)
            if res.get("ok"):
                self.state.chart.add_trade_marker(ts_iso, price, "SELL")
                
                # Calculate PnL for this trade
                if self.state.portfolio.avg_cost > 0:
                    pnl = (price - self.state.portfolio.avg_cost) * qty
                    self.state.log(f"🔴 AGENT SELL {qty} @ ₹{price} [{ts_iso}] - PnL: ₹{pnl:.2f} - Remaining: {self.state.portfolio.shares}")
                    
                    # Track trade for learning
                    trade_data = {
                        'timestamp': ts_iso,
                        'side': 'SELL',
                        'qty': qty,
                        'price': price,
                        'pnl': pnl,
                        'avg_cost': self.state.portfolio.avg_cost
                    }
                    self.state.trading_memory.add_trade(trade_data)
                else:
                    self.state.log(f"🔴 AGENT SELL {qty} @ ₹{price} [{ts_iso}] - Remaining: {self.state.portfolio.shares}")
        else:
            return {"ok": False, "reason": "Invalid side"}
        
        return {"ok": True, "portfolio": self.tool_portfolio_state()}

    def tool_get_next_open_volume(self) -> Dict[str, Any]:
        """Enhanced next bar data with technical indicators."""
        nxt = self.state.stream.peek_next_open_volume()
        if not nxt:
            return {"done": True}
        
        ts, o, v = nxt
        self.state.portfolio.mark(o)
        
        # Calculate technical indicators from historical data
        tech_indicators = self._calculate_technical_indicators(o, v)
        
        # Store this bar data for learning
        bar_data = {
            'timestamp': ts.isoformat(),
            'open': o,
            'volume': v,
            'indicators': tech_indicators
        }
        self.state.historical_data.append(bar_data)
        
        return {
            "done": False, 
            "ts": ts.isoformat(), 
            "open": o, 
            "volume": v,
            "technical_indicators": tech_indicators,
            "bars_processed": len(self.state.historical_data)
        }

    def tool_on_bar_close(self) -> Dict[str, Any]:
        """Enhanced bar close with learning updates."""
        res = self.state.stream.commit_close_and_advance()
        if not res:
            return {"done": True}
        
        ts, close_val = res
        o = self.state.portfolio.last_price
        self.state.chart.append_live_candle(ts, o, close_val)
        self.state.portfolio.mark(close_val)
        
        # Update the last bar with close price
        if self.state.historical_data:
            self.state.historical_data[-1]['close'] = close_val
            self.state.historical_data[-1]['bar_pnl'] = close_val - o
        
        snap = self.tool_portfolio_state()
        
        # Enhanced logging with performance metrics
        perf = self.state.trading_memory.get_recent_performance(5)
        win_rate = perf.get('recent_win_rate', 0) * 100
        
        self.state.log(f"📊 BAR CLOSE {ts.strftime('%H:%M')} O={o:.2f} C={close_val:.2f} | "
                      f"Cash=₹{snap['cash']} Shares={snap['shares']} PnL=₹{snap['total_pnl']} | "
                      f"Win Rate: {win_rate:.1f}%")
        
        return {
            "done": False, 
            "ts": ts.isoformat(), 
            "close": close_val, 
            "portfolio": snap,
            "performance": perf
        }

    def _calculate_technical_indicators(self, current_open: float, current_volume: float) -> Dict:
        """Calculate technical indicators from historical data."""
        if len(self.state.historical_data) < 10:
            return {"insufficient_data": True}
        
        # Get recent close prices and volumes
        recent_bars = self.state.historical_data[-20:] if len(self.state.historical_data) >= 20 else self.state.historical_data
        closes = [bar.get('close', bar.get('open', 0)) for bar in recent_bars if bar.get('close') is not None]
        volumes = [bar.get('volume', 0) for bar in recent_bars]
        
        if len(closes) < 5:
            return {"insufficient_data": True}
        
        # Simple moving averages
        sma_5 = sum(closes[-5:]) / 5 if len(closes) >= 5 else closes[-1]
        sma_10 = sum(closes[-10:]) / 10 if len(closes) >= 10 else sma_5
        sma_20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else sma_10
        
        # Volume analysis
        avg_volume = sum(volumes) / len(volumes) if volumes else 1
        volume_spike = current_volume / avg_volume if avg_volume > 0 else 1
        
        # Momentum
        momentum = (current_open - closes[-1]) / closes[-1] * 100 if closes[-1] > 0 else 0
        price_vs_sma5 = (current_open - sma_5) / sma_5 * 100 if sma_5 > 0 else 0
        
        return {
            "sma_5": round(sma_5, 2),
            "sma_10": round(sma_10, 2), 
            "sma_20": round(sma_20, 2),
            "momentum_pct": round(momentum, 2),
            "price_vs_sma5_pct": round(price_vs_sma5, 2),
            "volume_spike": round(volume_spike, 2),
            "avg_volume": round(avg_volume, 0),
            "trend_signal": "BULLISH" if current_open > sma_5 > sma_10 else "BEARISH" if current_open < sma_5 < sma_10 else "NEUTRAL"
        }

    # NEW: Manual override methods (kept for UI compatibility)
    def manual_sell_all_shares(self, current_price: float, ts_iso: str) -> Dict[str, Any]:
        """MANUAL OVERRIDE: Sell all shares immediately"""
        snap = self.state.portfolio.snapshot()
        current_shares = snap["shares"]
        
        if current_shares > 0:
            result = self.tool_place_order("SELL", current_shares, current_price, ts_iso)
            self.state.manual_sell_all = False
            return {"executed": True, "action": "SELL_ALL", "shares": current_shares, "result": result}
        else:
            self.state.manual_sell_all = False
            return {"executed": False, "reason": "No shares to sell"}

    def manual_buy_max_shares(self, current_price: float, ts_iso: str) -> Dict[str, Any]:
        """MANUAL OVERRIDE: Buy maximum shares with available cash"""
        snap = self.state.portfolio.snapshot()
        available_cash = snap["cash"]
        
        if available_cash >= current_price:
            target_cash = available_cash * 0.95
            max_qty = max(1, int(target_cash / current_price))
            
            result = self.tool_place_order("BUY", max_qty, current_price, ts_iso)
            self.state.manual_buy_max = False
            return {"executed": True, "action": "BUY_MAX", "shares": max_qty, "result": result}
        else:
            self.state.manual_buy_max = False
            return {"executed": False, "reason": "Insufficient cash"}

    def set_manual_sell_all(self):
        """Trigger manual sell all shares"""
        self.state.manual_sell_all = True
        self.state.log("🚨 MANUAL SELL ALL TRIGGERED - Will execute on next step")

    def set_manual_buy_max(self):
        """Trigger manual buy maximum shares"""
        self.state.manual_buy_max = True
        self.state.log("🚨 MANUAL BUY MAX TRIGGERED - Will execute on next step")

    # ------------------------
    # Set up / session
    # ------------------------
    def initialize(self, ticker: str, starting_cash: float) -> Dict[str, Any]:
        data_dir = Path("data")
        df, csv_path = download_and_prepare(ticker, data_dir)
        stream = StreamCursor(df)

        state = AppState(
            ticker=ticker, data_df=df, csv_path=csv_path, stream=stream,
            portfolio=Portfolio(cash=float(starting_cash))
        )
        state.chart.init_context(stream.get_context_df())
        state.log(f"🚀 INTELLIGENT TRADER READY: {csv_path.name} | Starting Capital: ₹{starting_cash}")
        state.log(f"📊 Context day plotted - Trading starts with next available day")
        state.log(f"🎯 AGGRESSIVE MODE: Up to 90% capital deployment, intelligent learning system active")

        self.state = state

        # Build enhanced LLM agent with learning tools
        if self.use_llm:
            tools = [
                FunctionTool(self.tool_get_next_open_volume, description="Get next 1m bar's Open, Volume & technical indicators."),
                FunctionTool(self.tool_get_trading_memory, description="Access complete trading history and performance metrics for learning."),
                FunctionTool(self.tool_place_order, description="Place aggressive long-only order (BUY/SELL integer qty at current Open)."),
                FunctionTool(self.tool_on_bar_close, description="Reveal bar Close, update chart & track performance."),
                FunctionTool(self.tool_portfolio_state, description="Get detailed portfolio status with utilization metrics."),
            ]

            self.agent = AssistantAgent(
                name="IntelligentTrader",
                model_client=self.model_client,
                tools=tools,
                system_message=_make_intelligent_policy_prompt(ticker)
            )
        
        return {
            "fig": state.chart.to_json(),
            "csv_path": str(csv_path),
            "logs": state.logs[-10:],
            "portfolio": state.portfolio.snapshot()
        }

    # ------------------------
    # Enhanced decision making per bar
    # ------------------------
    def _aggressive_intelligent_policy(self, o: float, v: float, hist: pd.DataFrame) -> Tuple[str, int, str]:
        """
        Enhanced deterministic policy: Aggressive, intelligent, learning from patterns.
        Uses technical indicators, volume analysis, and position sizing.
        """
        if len(self.state.historical_data) < 5:
            return "HOLD", 0, "insufficient_history"
        
        # Calculate technical indicators
        tech = self._calculate_technical_indicators(o, v)
        if tech.get("insufficient_data"):
            return "HOLD", 0, "insufficient_technical_data"
        
        # Get performance metrics for adaptive behavior
        perf = self.state.trading_memory.get_recent_performance(10)
        win_rate = perf.get('recent_win_rate', 0.5)
        
        # Portfolio analysis
        snap = self.state.portfolio.snapshot()
        available_cash = snap["cash"]
        current_shares = snap["shares"]
        total_value = available_cash + current_shares * o
        
        # Adaptive position sizing based on performance
        if win_rate > 0.6:  # High win rate - be more aggressive
            max_position_pct = 0.5  # 50% max per trade
            cash_utilization_target = 0.9  # Use up to 90% of capital
        elif win_rate > 0.4:  # Decent win rate - moderate aggression
            max_position_pct = 0.35  # 35% max per trade  
            cash_utilization_target = 0.7  # Use up to 70% of capital
        else:  # Low win rate - be more conservative
            max_position_pct = 0.25  # 25% max per trade
            cash_utilization_target = 0.5  # Use up to 50% of capital
        
        # Strong buy signals (aggressive entry)
        strong_buy_signals = (
            tech["trend_signal"] == "BULLISH" and
            tech["volume_spike"] > 1.5 and
            tech["momentum_pct"] > 0.1 and
            tech["price_vs_sma5_pct"] > 0.05
        )
        
        # Medium buy signals
        medium_buy_signals = (
            tech["trend_signal"] != "BEARISH" and
            tech["volume_spike"] > 1.2 and
            tech["momentum_pct"] > 0
        )
        
        # Exit signals
        exit_signals = (
            tech["trend_signal"] == "BEARISH" or
            tech["momentum_pct"] < -0.15 or
            (current_shares > 0 and snap["unrealized_pnl"] < -0.02 * snap["avg_cost"] * current_shares)  # 2% stop loss
        )
        
        # Decision logic
        max_buy_cash = min(available_cash * max_position_pct, 
                          max(0, total_value * cash_utilization_target - current_shares * o))
        max_shares = int(max_buy_cash // o) if o > 0 else 0
        
        # BUY decisions
        if current_shares == 0 and strong_buy_signals and max_shares >= 1:
            # High conviction entry - use larger position
            qty = min(max_shares, max(1, int(max_buy_cash // o)))
            return "BUY", qty, f"strong_buy_signal_wr_{win_rate:.2f}"
            
        elif current_shares == 0 and medium_buy_signals and max_shares >= 1:
            # Medium conviction entry - smaller position
            qty = min(max_shares // 2, max(1, int(max_buy_cash // (2 * o))))
            return "BUY", qty, f"medium_buy_signal_wr_{win_rate:.2f}"
            
        # Scale into winning positions
        elif current_shares > 0 and snap["unrealized_pnl"] > 0 and strong_buy_signals and max_shares >= 1:
            qty = min(max_shares // 3, max(1, current_shares // 4))  # Add 25% to position
            return "BUY", qty, f"scale_into_winner_pnl_{snap['unrealized_pnl']:.2f}"
        
        # SELL decisions
        elif current_shares > 0 and exit_signals:
            # Full exit on strong negative signals
            return "SELL", current_shares, f"exit_signal_pnl_{snap['unrealized_pnl']:.2f}"
            
        # Take partial profits on big winners
        elif current_shares > 0 and snap["unrealized_pnl"] > 0.03 * snap["avg_cost"] * current_shares:  # 3%+ gain
            qty = max(1, current_shares // 3)  # Sell 1/3 position
            return "SELL", qty, f"partial_profit_pnl_{snap['unrealized_pnl']:.2f}"
        
        return "HOLD", 0, f"no_clear_edge_trend_{tech['trend_signal']}_vol_{tech['volume_spike']:.1f}"

    def step_once(self) -> Dict[str, Any]:
        """
        Enhanced one full 1m step with intelligent learning and decision making.
        """
        if self.state is None:
            return {"done": True}

        # Check if more bars available
        check = self.tool_get_next_open_volume()
        if check.get("done"):
            # Trading complete - show final summary
            if hasattr(self.state, 'portfolio'):
                final_snap = self.tool_portfolio_state()
                memory = self.state.trading_memory
                self.state.log(f"🏁 TRADING COMPLETE!")
                self.state.log(f"📈 FINAL RESULTS: PnL=₹{final_snap.get('total_pnl', 0)} | "
                              f"Total Trades: {len(memory.trade_history)} | "
                              f"Win Rate: {memory.performance_metrics.get('win_rate', 0)*100:.1f}%")
            return {"done": True}

        ts_iso = check["ts"]
        o = float(check["open"])
        v = float(check["volume"])
        tech = check.get("technical_indicators", {})

        # Check for manual overrides first
        manual_result = None
        if self.state.manual_sell_all:
            manual_result = self.manual_sell_all_shares(o, ts_iso)
        elif self.state.manual_buy_max:
            manual_result = self.manual_buy_max_shares(o, ts_iso)

        # If no manual override, proceed with agent/fallback decision
        if not manual_result or not manual_result.get("executed"):
            # Enhanced decision making with LLM or fallback
            if self.use_llm and self.agent:
                # Provide rich context to LLM
                try:
                    memory_data = self.tool_get_trading_memory()
                    portfolio_data = self.tool_portfolio_state()
                    
                    prompt = f"""
🎯 NEXT BAR ANALYSIS:
Timestamp: {ts_iso}
Open: ₹{o} | Volume: {v:,.0f}

📊 TECHNICAL INDICATORS:
{json.dumps(tech, indent=2)}

💼 CURRENT PORTFOLIO:
{json.dumps(portfolio_data, indent=2)}

🧠 TRADING MEMORY & PERFORMANCE:
{json.dumps(memory_data, indent=2)}

DECISION TIME: Analyze this setup with your complete trading history and technical signals.
Be AGGRESSIVE but INTELLIGENT. Use your learning to make the best trade decision.
Remember: You can use up to 90% of capital, scale into winners, cut losses quickly.

You MUST:
1. Call get_next_open_volume() (already done)
2. Call get_trading_memory() (already done) 
3. Call place_order() if you want to trade
4. Call on_bar_close() to complete the bar

MAKE YOUR DECISION NOW!
"""
                    
                    message = TextMessage(content=prompt, source="user")
                    # Use sync call to agent
                    response = asyncio.run(self._get_agent_response(message))
                    
                except Exception as e:
                    self.state.log(f"⚠️ Agent error, using fallback: {str(e)}")
                    # Use fallback policy
                    hist = self.state.stream.get_context_df().copy()
                    action, qty, reason = self._aggressive_intelligent_policy(o, v, hist)
                    
                    if action != "HOLD" and qty > 0:
                        self.tool_place_order(action, qty, o, ts_iso)
                    else:
                        self.state.log(f"⏸️ FALLBACK HOLD - {reason} | Open=₹{o} Volume={v:,.0f}")
            else:
                # Enhanced deterministic fallback policy
                hist = self.state.stream.get_context_df().copy()
                action, qty, reason = self._aggressive_intelligent_policy(o, v, hist)
                
                if action != "HOLD" and qty > 0:
                    self.tool_place_order(action, qty, o, ts_iso)
                else:
                    self.state.log(f"⏸️ HOLD - {reason} | Open=₹{o} Volume={v:,.0f}")
        
        # Always reveal close
        close_result = self.tool_on_bar_close()
        
        result = {
            "done": close_result.get("done", False),
            "fig": self.state.chart.to_json(),
            "logs": self.state.logs[-200:],
            "portfolio": self.tool_portfolio_state()
        }
        
        if manual_result:
            result["manual_override"] = manual_result
            
        return result

    async def _get_agent_response(self, message):
        """Get response from the enhanced AutoGen agent"""
        try:
            response = await self.agent.on_messages([message], cancellation_token=None)
            return response
        except Exception as e:
            # Let the error propagate to trigger fallback
            raise e