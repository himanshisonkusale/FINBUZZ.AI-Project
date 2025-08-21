# charting.py
from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go


class Candles:
    def __init__(self):
        self.fig = go.Figure()

    def init_context(self, context_df: pd.DataFrame):
        # Enhanced premium candlestick styling
        self.fig = go.Figure(data=[go.Candlestick(
            x=context_df.index,
            open=context_df["Open"],
            high=context_df["Open"].combine(context_df["Close"], max),
            low=context_df["Open"].combine(context_df["Close"], min),
            close=context_df["Close"],
            name="Context (Historical)",
            increasing_line_color='#00ff88',      # Bright green
            decreasing_line_color='#ff4444',      # Bright red
            increasing_fillcolor='rgba(0, 255, 136, 0.8)',
            decreasing_fillcolor='rgba(255, 68, 68, 0.8)',
            line=dict(width=2),
            whiskerwidth=0.8,
            opacity=0.9
        )])
        
        # Premium dark theme with enhanced styling
        self.fig.update_layout(
            title=dict(
                text="🚀 AI Trading Agent - Premium Market Analysis",
                font=dict(size=20, color='#00ff88', family='JetBrains Mono'),
                x=0.5
            ),
            margin=dict(l=60, r=60, t=80, b=60),
            height=600,
            xaxis_title=dict(
                text="⏰ Time (IST)",
                font=dict(size=14, color='#ffffff', family='JetBrains Mono')
            ),
            yaxis_title=dict(
                text="💰 Price (₹)",
                font=dict(size=14, color='#ffffff', family='JetBrains Mono')
            ),
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            paper_bgcolor='#0a0a0a',
            plot_bgcolor='#1a1a1a',
            font=dict(
                family="JetBrains Mono",
                size=12,
                color="#ffffff"
            ),
            xaxis=dict(
                gridcolor='#333333',
                gridwidth=1,
                color='#ffffff',
                showgrid=True,
                zeroline=False,
                tickfont=dict(size=10, color='#cccccc')
            ),
            yaxis=dict(
                gridcolor='#333333',
                gridwidth=1,
                color='#ffffff',
                showgrid=True,
                zeroline=False,
                tickfont=dict(size=10, color='#cccccc'),
                tickformat=".2f"
            ),
            legend=dict(
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00ff88',
                borderwidth=1,
                font=dict(color='#ffffff', size=12),
                x=0.02,
                y=0.98
            ),
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor='rgba(0, 0, 0, 0.8)',
                bordercolor='#00ff88',
                font=dict(size=12, color='white', family='JetBrains Mono')
            )
        )
        
        # Add enhanced grid and styling
        self.fig.update_xaxes(
            showspikes=True,
            spikecolor="#00ff88",
            spikesnap="cursor",
            spikemode="across",
            spikethickness=1
        )
        
        self.fig.update_yaxes(
            showspikes=True,
            spikecolor="#00ff88",
            spikesnap="cursor",
            spikemode="across",
            spikethickness=1
        )
        
        # Set initial zoom to show data properly with padding
        if not context_df.empty:
            y_min = context_df[["Open", "Close"]].min().min()
            y_max = context_df[["Open", "Close"]].max().max()
            y_range = y_max - y_min
            self.fig.update_yaxes(
                range=[y_min - y_range * 0.05, y_max + y_range * 0.05]
            )

    def append_live_candle(self, ts, o, c):
        # Enhanced live candles with premium styling
        high_val = max(o, c)
        low_val = min(o, c)
        
        # Determine color based on price movement
        is_bullish = c > o
        candle_color = '#00ffff' if is_bullish else '#ff6600'
        fill_color = 'rgba(0, 255, 255, 0.7)' if is_bullish else 'rgba(255, 102, 0, 0.7)'
        
        self.fig.add_candlestick(
            x=[ts],
            open=[o],
            high=[high_val],
            low=[low_val],
            close=[c],
            name="Live Trading",
            increasing_line_color='#00ffff',
            decreasing_line_color='#ff6600',
            increasing_fillcolor='rgba(0, 255, 255, 0.7)',
            decreasing_fillcolor='rgba(255, 102, 0, 0.7)',
            line=dict(width=2),
            whiskerwidth=0.8,
            opacity=0.9,
            showlegend=False
        )
        
        # Update y-axis range dynamically for better visualization
        current_data = self.fig.data
        all_highs = []
        all_lows = []
        
        for trace in current_data:
            if hasattr(trace, 'high') and trace.high is not None:
                all_highs.extend([h for h in trace.high if h is not None])
            if hasattr(trace, 'low') and trace.low is not None:
                all_lows.extend([l for l in trace.low if l is not None])
        
        if all_highs and all_lows:
            y_min = min(all_lows)
            y_max = max(all_highs)
            y_range = y_max - y_min
            self.fig.update_yaxes(
                range=[y_min - y_range * 0.03, y_max + y_range * 0.03]
            )

    def add_trade_marker(self, ts, price, side: str):
        if side == "BUY":
            # Enhanced BUY marker with glow effect
            self.fig.add_trace(go.Scatter(
                x=[ts], y=[price],
                mode="markers+text",
                marker=dict(
                    symbol="triangle-up",
                    size=20,
                    color="lime",
                    line=dict(width=3, color="white"),
                    opacity=0.9
                ),
                text=["BUY"],
                textposition="top center",
                textfont=dict(
                    size=10,
                    color="lime",
                    family="JetBrains Mono"
                ),
                name="Buy Signal",
                showlegend=False,
                hovertemplate="<b>BUY ORDER</b><br>" +
                            "Time: %{x}<br>" +
                            "Price: ₹%{y:.2f}<br>" +
                            "<extra></extra>"
            ))
            
            # Add subtle glow effect
            self.fig.add_trace(go.Scatter(
                x=[ts], y=[price],
                mode="markers",
                marker=dict(
                    symbol="triangle-up",
                    size=35,
                    color="lime",
                    opacity=0.3
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
            
        else:  # SELL
            # Enhanced SELL marker with glow effect
            self.fig.add_trace(go.Scatter(
                x=[ts], y=[price],
                mode="markers+text",
                marker=dict(
                    symbol="triangle-down",
                    size=20,
                    color="red",
                    line=dict(width=3, color="white"),
                    opacity=0.9
                ),
                text=["SELL"],
                textposition="bottom center",
                textfont=dict(
                    size=10,
                    color="red",
                    family="JetBrains Mono"
                ),
                name="Sell Signal",
                showlegend=False,
                hovertemplate="<b>SELL ORDER</b><br>" +
                            "Time: %{x}<br>" +
                            "Price: ₹%{y:.2f}<br>" +
                            "<extra></extra>"
            ))
            
            # Add subtle glow effect
            self.fig.add_trace(go.Scatter(
                x=[ts], y=[price],
                mode="markers",
                marker=dict(
                    symbol="triangle-down",
                    size=35,
                    color="red",
                    opacity=0.3
                ),
                showlegend=False,
                hoverinfo='skip'
            ))

    def add_volume_bar(self, ts, volume, color='rgba(100, 100, 100, 0.5)'):
        """Add volume bars at the bottom of the chart"""
        # This could be extended to show volume data
        pass

    def add_technical_indicator(self, ts_list, values, name, color='#ffff00'):
        """Add technical indicators like moving averages"""
        self.fig.add_trace(go.Scatter(
            x=ts_list,
            y=values,
            mode='lines',
            name=name,
            line=dict(color=color, width=2, dash='dot'),
            opacity=0.8,
            showlegend=True
        ))

    def add_support_resistance(self, price_level, label, color='#ff00ff'):
        """Add support/resistance lines"""
        self.fig.add_hline(
            y=price_level,
            line_dash="dash",
            line_color=color,
            line_width=2,
            opacity=0.7,
            annotation_text=label,
            annotation_position="top right"
        )

    def to_json(self):
        # Return the enhanced figure for Gradio
        return self.fig