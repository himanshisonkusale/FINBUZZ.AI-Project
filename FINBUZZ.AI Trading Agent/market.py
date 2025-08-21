# market.py
from __future__ import annotations
import pandas as pd
import numpy as np
import yfinance as yf
from pathlib import Path
from typing import Iterator, Tuple, Optional
import pytz
from datetime import datetime, time, timedelta


IST = pytz.timezone("Asia/Kolkata")
MARKET_START = time(9, 15)
MARKET_END = time(15, 30)

# Use current date - 10 days for more realistic trading
current_date = pd.Timestamp.now(tz=IST)
START_DATE = current_date - pd.Timedelta(days=10)
END_DATE = current_date - pd.Timedelta(days=1)  # Yesterday as end


def _to_ist(df: pd.DataFrame) -> pd.DataFrame:
    idx = df.index
    if idx.tz is None:
        # yfinance usually returns UTC tz-aware (sometimes naive). Assume UTC if naive.
        idx = idx.tz_localize("UTC")
    df = df.copy()
    df.index = idx.tz_convert(IST)
    return df


def _market_hours_filter(df: pd.DataFrame) -> pd.DataFrame:
    # Keep only 09:15-15:30 IST bars
    mask = (df.index.time >= MARKET_START) & (df.index.time <= MARKET_END)
    return df.loc[mask]


def _slice_recent_days(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[(df.index >= START_DATE) & (df.index <= END_DATE)]


def download_and_prepare(ticker: str, data_dir: Path) -> Tuple[pd.DataFrame, Path]:
    """
    Downloads recent 10d-5m data, converts to IST, filters to last 10 trading days, market hours,
    saves CSV with Open,Close,Volume only, returns filtered OHLCV df and csv path.
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Get more data to ensure we have enough after filtering
    df = yf.download(ticker, period="1mo", interval="5m", auto_adjust=False, progress=False)
    if df is None or df.empty:
        raise ValueError(f"No data returned for {ticker} using 1mo/5m.")

    # Handle MultiIndex columns that yfinance sometimes returns
    if hasattr(df.columns, 'nlevels') and df.columns.nlevels > 1:
        # If MultiIndex, flatten it by taking the first level
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    df = _to_ist(df)
    df = _market_hours_filter(df)
    df = _slice_recent_days(df)
    
    if df.empty:
        raise ValueError("Filtered data is empty after restricting to recent trading days.")

    # Create a mapping of lowercase to actual column names
    col_mapping = {}
    for col in df.columns:
        col_str = str(col)
        col_mapping[col_str.lower()] = col_str
    
    # Check and rename required columns
    required_columns = ["Open", "Close", "Volume"]
    for required in required_columns:
        required_lower = required.lower()
        
        if required in df.columns:
            # Column already exists with correct case
            continue
        elif required_lower in col_mapping:
            # Found column with different case - rename it
            actual_col = col_mapping[required_lower]
            if actual_col != required:
                df[required] = df[actual_col]
        else:
            # Column not found at all
            available_cols = list(df.columns)
            raise ValueError(f"Column '{required}' missing in data. Available columns: {available_cols}")

    csv_df = df[["Open", "Close", "Volume"]].copy()
    start_str = START_DATE.strftime("%Y-%m-%d")
    end_str = END_DATE.strftime("%Y-%m-%d")
    csv_path = data_dir / f"{ticker.replace('.', '_')}_5m_{start_str}_to_{end_str}.csv"
    csv_df.to_csv(csv_path, index_label="Datetime")

    return df, csv_path


class StreamCursor:
    """
    Handles the trading stream:
    - Show first trading day in market preview (context)
    - Start actual trading from second day
    - Stream through remaining trading days
    """
    def __init__(self, df: pd.DataFrame):
        # Sort by time and split data
        df = df.sort_index()
        
        # Get unique trading days
        unique_dates = df.index.date
        trading_days = sorted(set(unique_dates))
        
        if len(trading_days) < 2:
            # If only one day, show it as context and trade on same day
            first_day = trading_days[0]
            self.context_df = df[df.index.date == first_day].copy()
            self.trade_df = df.copy()
        else:
            # Show first day as context, trade from second day onwards
            first_day = trading_days[0]
            self.context_df = df[df.index.date == first_day].copy()
            self.trade_df = df[df.index.date != first_day].copy()
        
        # Iterator state for trading data
        self._iter_idx = 0
        self._times = self.trade_df.index.to_list()

    def get_context_df(self) -> pd.DataFrame:
        # Return first day data for market preview
        return self.context_df

    def has_next(self) -> bool:
        return self._iter_idx < len(self._times)

    def peek_next_open_volume(self) -> Optional[Tuple[pd.Timestamp, float, float]]:
        if not self.has_next():
            return None
        ts = self._times[self._iter_idx]
        row = self.trade_df.loc[ts]
        return ts, float(row["Open"]), float(row["Volume"])

    def commit_close_and_advance(self) -> Optional[Tuple[pd.Timestamp, float]]:
        """
        Reveal the close for the current bar, then advance to the next.
        """
        if self._iter_idx >= len(self._times):
            return None
        ts = self._times[self._iter_idx]
        close_val = float(self.trade_df.loc[ts]["Close"])
        self._iter_idx += 1
        return ts, close_val

    def get_bar(self, ts: pd.Timestamp) -> pd.Series:
        return self.trade_df.loc[ts]