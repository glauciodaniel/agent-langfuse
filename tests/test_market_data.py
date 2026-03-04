"""
Testes para o modulo de dados de mercado.

Estes testes NAO requerem API da OpenAI.
"""

import sys
from pathlib import Path

# Adicionar raiz ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from domain.market_data import (
    get_stock_price,
    compare_stocks,
    get_market_summary,
    calculate_investment_returns,
    get_available_tickers,
)


def test_get_stock_price_valid():
    """Testa preco com ticker valido."""
    result = get_stock_price("PETR4")
    assert result == "R$ 38.50"
    
    # Minusculo tambem funciona
    result = get_stock_price("petr4")
    assert result == "R$ 38.50"


def test_get_stock_price_invalid():
    """Testa preco com ticker invalido."""
    result = get_stock_price("INVALID")
    assert "nao encontrado" in result.lower()


def test_compare_stocks_valid():
    """Testa comparacao valida."""
    result = compare_stocks("PETR4", "VALE3")
    assert "PETR4" in result
    assert "VALE3" in result
    assert "COMPARACAO" in result.upper()


def test_compare_stocks_invalid():
    """Testa comparacao com ticker invalido."""
    result = compare_stocks("PETR4", "INVALID")
    assert "nao encontrado" in result.lower()


def test_market_summary():
    """Testa resumo do mercado."""
    result = get_market_summary()
    assert "IBOV" in result
    assert "ALTAS" in result.upper()
    assert "BAIXAS" in result.upper()


def test_calculate_returns_valid():
    """Testa calculo de rendimentos valido."""
    result = calculate_investment_returns("PETR4", 10000, 12)
    assert "PETR4" in result
    assert "R$" in result
    assert "SIMULACAO" in result.upper()


def test_calculate_returns_invalid_value():
    """Testa calculo com valor invalido."""
    result = calculate_investment_returns("PETR4", -100, 12)
    assert "maior que zero" in result.lower()


def test_calculate_returns_invalid_period():
    """Testa calculo com periodo invalido."""
    result = calculate_investment_returns("PETR4", 10000, 0)
    assert "periodo" in result.lower()


def test_available_tickers():
    """Testa listagem de tickers."""
    tickers = get_available_tickers()
    assert "PETR4" in tickers
    assert "VALE3" in tickers
    assert "ITUB4" in tickers
    assert len(tickers) >= 4


if __name__ == "__main__":
    # Rodar testes simples
    tests = [
        test_get_stock_price_valid,
        test_get_stock_price_invalid,
        test_compare_stocks_valid,
        test_compare_stocks_invalid,
        test_market_summary,
        test_calculate_returns_valid,
        test_calculate_returns_invalid_value,
        test_calculate_returns_invalid_period,
        test_available_tickers,
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
