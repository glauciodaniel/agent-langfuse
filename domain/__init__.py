"""Modulo de dominio - dados de mercado e ferramentas."""

from domain.tools import (
    stock_price_tool,
    compare_stocks_tool,
    market_summary_tool,
    calculate_returns_tool,
    list_available_stocks_tool,
    ALL_TOOLS,
)
from domain.market_data import (
    MOCK_STOCK_DATA,
    MOCK_MARKET_INDICES,
    get_stock_price,
    compare_stocks,
    get_market_summary,
    calculate_investment_returns,
    get_available_tickers,
)

__all__ = [
    # Tools
    "stock_price_tool",
    "compare_stocks_tool",
    "market_summary_tool",
    "calculate_returns_tool",
    "list_available_stocks_tool",
    "ALL_TOOLS",
    # Market Data
    "MOCK_STOCK_DATA",
    "MOCK_MARKET_INDICES",
    "get_stock_price",
    "compare_stocks",
    "get_market_summary",
    "calculate_investment_returns",
    "get_available_tickers",
]
