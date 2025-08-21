# portfolio.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class Fill:
    ts: str
    side: str  # "BUY" or "SELL"
    qty: int
    price: float


@dataclass
class Portfolio:
    cash: float
    shares: int = 0
    avg_cost: float = 0.0
    realized_pnl: float = 0.0
    last_price: float = 0.0
    trade_log: List[Fill] = field(default_factory=list)

    def value(self) -> float:
        return self.cash + self.shares * self.last_price

    def total_pnl(self) -> float:
        return self.realized_pnl + self.unrealized_pnl()

    def unrealized_pnl(self) -> float:
        return (self.last_price - self.avg_cost) * self.shares if self.shares > 0 else 0.0

    def can_buy(self, qty: int, price: float) -> bool:
        return qty > 0 and self.cash >= qty * price

    def can_sell(self, qty: int) -> bool:
        return qty > 0 and qty <= self.shares

    def buy(self, ts: str, qty: int, price: float) -> Dict:
        if not self.can_buy(qty, price):
            return {"ok": False, "reason": "Insufficient cash or invalid qty"}
        cost = qty * price
        # update avg cost
        new_total_cost = self.avg_cost * self.shares + cost
        new_shares = self.shares + qty
        self.avg_cost = new_total_cost / new_shares if new_shares > 0 else 0.0
        self.shares = new_shares
        self.cash -= cost
        self.trade_log.append(Fill(ts=ts, side="BUY", qty=qty, price=price))
        return {"ok": True}

    def sell(self, ts: str, qty: int, price: float) -> Dict:
        if not self.can_sell(qty):
            return {"ok": False, "reason": "Insufficient shares or invalid qty"}
        proceeds = qty * price
        # realized pnl on portion sold
        self.realized_pnl += (price - self.avg_cost) * qty
        self.shares -= qty
        self.cash += proceeds
        if self.shares == 0:
            self.avg_cost = 0.0
        self.trade_log.append(Fill(ts=ts, side="SELL", qty=qty, price=price))
        return {"ok": True}

    def mark(self, price: float):
        self.last_price = price

    def snapshot(self) -> Dict:
        return {
            "cash": round(self.cash, 2),
            "shares": int(self.shares),
            "avg_cost": round(self.avg_cost, 4),
            "last_price": round(self.last_price, 4),
            "realized_pnl": round(self.realized_pnl, 2),
            "unrealized_pnl": round(self.unrealized_pnl(), 2),
            "total_pnl": round(self.total_pnl(), 2),
        }
