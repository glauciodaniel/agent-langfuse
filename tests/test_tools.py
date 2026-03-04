"""
Testes para as ferramentas LangChain.

Estes testes NAO requerem API da OpenAI (testam as tools diretamente).
"""

import sys
from pathlib import Path

# Adicionar raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from domain.tools import (
    stock_price_tool,
    compare_stocks_tool,
    market_summary_tool,
    calculate_returns_tool,
    list_available_stocks_tool,
    ALL_TOOLS,
)


def test_stock_price_tool():
    """Testa tool de preco."""
    result = stock_price_tool.invoke({"ticker": "PETR4"})
    assert "R$" in result


def test_compare_stocks_tool():
    """Testa tool de comparacao."""
    result = compare_stocks_tool.invoke({"ticker1": "ITUB4", "ticker2": "BBDC4"})
    assert "ITUB4" in result
    assert "BBDC4" in result


def test_market_summary_tool():
    """Testa tool de resumo."""
    result = market_summary_tool.invoke({})
    assert "IBOV" in result


def test_calculate_returns_tool():
    """Testa tool de calculo."""
    result = calculate_returns_tool.invoke({
        "ticker": "VALE3",
        "initial_investment": 5000,
        "months": 6
    })
    assert "VALE3" in result
    assert "R$" in result


def test_list_stocks_tool():
    """Testa tool de listagem."""
    result = list_available_stocks_tool.invoke({})
    assert "PETR4" in result


def test_all_tools_list():
    """Testa que ALL_TOOLS contem todas as ferramentas."""
    assert len(ALL_TOOLS) == 5
    
    tool_names = [t.name for t in ALL_TOOLS]
    assert "stock_price_tool" in tool_names
    assert "compare_stocks_tool" in tool_names
    assert "market_summary_tool" in tool_names
    assert "calculate_returns_tool" in tool_names
    assert "list_available_stocks_tool" in tool_names


if __name__ == "__main__":
    tests = [
        test_stock_price_tool,
        test_compare_stocks_tool,
        test_market_summary_tool,
        test_calculate_returns_tool,
        test_list_stocks_tool,
        test_all_tools_list,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"[PASSOU] {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"[FALHOU] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERRO] {test.__name__}: {e}")
            failed += 1
    
    print(f"\nTotal: {passed} passaram, {failed} falharam")
