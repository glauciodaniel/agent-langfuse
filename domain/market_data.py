"""
Mock de API de Mercado Financeiro

Este modulo simula uma API de cotacoes de acoes em tempo real.
Em um cenario real, isso seria substituido por uma integracao com APIs como
Yahoo Finance, Alpha Vantage, ou B3 (Bolsa brasileira).
"""

from typing import Optional
from datetime import datetime
import random

MOCK_STOCK_DATA = {
    "PETR4": {
        "price": 38.50,
        "name": "Petrobras",
        "sector": "Petroleo e Gas",
        "variation_24h": 2.35,
        "volume": 45_000_000,
        "dividend_yield": 12.5,
    },
    "VALE3": {
        "price": 60.20,
        "name": "Vale",
        "sector": "Mineracao",
        "variation_24h": -1.20,
        "volume": 38_000_000,
        "dividend_yield": 8.2,
    },
    "ITUB4": {
        "price": 32.10,
        "name": "Itau Unibanco",
        "sector": "Bancos",
        "variation_24h": 0.85,
        "volume": 25_000_000,
        "dividend_yield": 5.8,
    },
    "BBDC4": {
        "price": 14.85,
        "name": "Bradesco",
        "sector": "Bancos",
        "variation_24h": -0.45,
        "volume": 20_000_000,
        "dividend_yield": 6.2,
    },
    "WEGE3": {
        "price": 42.30,
        "name": "WEG",
        "sector": "Bens Industriais",
        "variation_24h": 1.50,
        "volume": 12_000_000,
        "dividend_yield": 1.5,
    },
    "ABEV3": {
        "price": 11.95,
        "name": "Ambev",
        "sector": "Bebidas",
        "variation_24h": 0.25,
        "volume": 30_000_000,
        "dividend_yield": 4.8,
    },
    "MGLU3": {
        "price": 2.15,
        "name": "Magazine Luiza",
        "sector": "Varejo",
        "variation_24h": -3.20,
        "volume": 55_000_000,
        "dividend_yield": 0.0,
    },
    "B3SA3": {
        "price": 12.45,
        "name": "B3",
        "sector": "Servicos Financeiros",
        "variation_24h": 0.95,
        "volume": 18_000_000,
        "dividend_yield": 7.1,
    },
}

MOCK_MARKET_INDICES = {
    "IBOV": {
        "name": "Ibovespa",
        "points": 128_450,
        "variation_24h": 0.85,
        "variation_week": 2.10,
        "variation_month": -1.35,
    },
    "IFIX": {
        "name": "Indice de Fundos Imobiliarios",
        "points": 3_245,
        "variation_24h": 0.25,
        "variation_week": 0.80,
        "variation_month": 1.20,
    },
    "SMLL": {
        "name": "Indice Small Cap",
        "points": 2_150,
        "variation_24h": -0.45,
        "variation_week": -1.20,
        "variation_month": -3.50,
    },
}


def get_stock_price(ticker: str) -> str:
    """Busca o preco simulado de uma acao pelo ticker."""
    ticker = ticker.upper()
    if ticker in MOCK_STOCK_DATA:
        price = MOCK_STOCK_DATA[ticker]["price"]
        return f"R$ {price:.2f}"
    else:
        available = ", ".join(MOCK_STOCK_DATA.keys())
        return f"Ticker {ticker} nao encontrado. Acoes disponiveis: {available}"


def get_stock_details(ticker: str) -> dict | str:
    """Retorna informacoes detalhadas de uma acao."""
    ticker = ticker.upper()
    if ticker in MOCK_STOCK_DATA:
        data = MOCK_STOCK_DATA[ticker]
        return {
            "ticker": ticker,
            "name": data["name"],
            "price": data["price"],
            "sector": data["sector"],
            "variation_24h": data["variation_24h"],
            "volume": data["volume"],
            "dividend_yield": data["dividend_yield"],
        }
    else:
        available = ", ".join(MOCK_STOCK_DATA.keys())
        return f"Ticker {ticker} nao encontrado. Acoes disponiveis: {available}"


def compare_stocks(ticker1: str, ticker2: str) -> str:
    """Compara duas acoes lado a lado."""
    ticker1 = ticker1.upper()
    ticker2 = ticker2.upper()
    
    if ticker1 not in MOCK_STOCK_DATA:
        available = ", ".join(MOCK_STOCK_DATA.keys())
        return f"Ticker {ticker1} nao encontrado. Acoes disponiveis: {available}"
    
    if ticker2 not in MOCK_STOCK_DATA:
        available = ", ".join(MOCK_STOCK_DATA.keys())
        return f"Ticker {ticker2} nao encontrado. Acoes disponiveis: {available}"
    
    s1 = MOCK_STOCK_DATA[ticker1]
    s2 = MOCK_STOCK_DATA[ticker2]
    
    lines = [
        f"COMPARACAO: {ticker1} vs {ticker2}",
        "",
        f"{ticker1} - {s1['name']}:",
        f"  - Preco: R$ {s1['price']:.2f}",
        f"  - Variacao 24h: {s1['variation_24h']:+.2f}%",
        f"  - Setor: {s1['sector']}",
        f"  - Dividend Yield: {s1['dividend_yield']:.1f}%",
        f"  - Volume: {s1['volume']:,}",
        "",
        f"{ticker2} - {s2['name']}:",
        f"  - Preco: R$ {s2['price']:.2f}",
        f"  - Variacao 24h: {s2['variation_24h']:+.2f}%",
        f"  - Setor: {s2['sector']}",
        f"  - Dividend Yield: {s2['dividend_yield']:.1f}%",
        f"  - Volume: {s2['volume']:,}",
        "",
        "ANALISE:",
        f"  - Maior preco: {ticker1 if s1['price'] > s2['price'] else ticker2}",
        f"  - Melhor performance 24h: {ticker1 if s1['variation_24h'] > s2['variation_24h'] else ticker2}",
        f"  - Maior dividend yield: {ticker1 if s1['dividend_yield'] > s2['dividend_yield'] else ticker2}",
    ]
    return "\n".join(lines)


def get_market_summary() -> str:
    """Retorna um resumo do mercado com indices e destaques."""
    sorted_by_variation = sorted(
        MOCK_STOCK_DATA.items(),
        key=lambda x: x[1]["variation_24h"],
        reverse=True
    )
    
    top_gainers = sorted_by_variation[:3]
    top_losers = sorted_by_variation[-3:][::-1]
    
    lines = [
        f"RESUMO DO MERCADO - {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
        "=" * 60,
        "INDICES PRINCIPAIS",
        "=" * 60,
    ]
    
    for code, data in MOCK_MARKET_INDICES.items():
        arrow = "[+]" if data["variation_24h"] >= 0 else "[-]"
        lines.append(f"{arrow} {data['name']} ({code}): {data['points']:,} pts ({data['variation_24h']:+.2f}%)")
    
    lines.extend([
        "",
        "=" * 60,
        "MAIORES ALTAS DO DIA",
        "=" * 60,
    ])
    
    for ticker, data in top_gainers:
        if data["variation_24h"] > 0:
            lines.append(f"[+] {ticker} ({data['name']}): R$ {data['price']:.2f} ({data['variation_24h']:+.2f}%)")
    
    lines.extend([
        "",
        "=" * 60,
        "MAIORES BAIXAS DO DIA",
        "=" * 60,
    ])
    
    for ticker, data in top_losers:
        if data["variation_24h"] < 0:
            lines.append(f"[-] {ticker} ({data['name']}): R$ {data['price']:.2f} ({data['variation_24h']:+.2f}%)")
    
    return "\n".join(lines)


def calculate_investment_returns(ticker: str, initial_investment: float, months: int) -> str:
    """Calcula rendimentos simulados de um investimento."""
    ticker = ticker.upper()
    
    if ticker not in MOCK_STOCK_DATA:
        available = ", ".join(MOCK_STOCK_DATA.keys())
        return f"Ticker {ticker} nao encontrado. Acoes disponiveis: {available}"
    
    if initial_investment <= 0:
        return "O valor do investimento deve ser maior que zero."
    
    if months <= 0 or months > 120:
        return "O periodo deve ser entre 1 e 120 meses."
    
    stock = MOCK_STOCK_DATA[ticker]
    
    sector_returns = {
        "Petroleo e Gas": 0.012,
        "Mineracao": 0.010,
        "Bancos": 0.008,
        "Bens Industriais": 0.015,
        "Bebidas": 0.006,
        "Varejo": 0.005,
        "Servicos Financeiros": 0.009,
    }
    
    monthly_return = sector_returns.get(stock["sector"], 0.008)
    dividend_monthly = stock["dividend_yield"] / 100 / 12
    
    total_return_rate = monthly_return + dividend_monthly
    final_value = initial_investment * ((1 + total_return_rate) ** months)
    
    total_gain = final_value - initial_investment
    percentage_gain = ((final_value / initial_investment) - 1) * 100
    
    cdi_monthly = 0.01
    cdi_final = initial_investment * ((1 + cdi_monthly) ** months)
    
    savings_monthly = 0.005
    savings_final = initial_investment * ((1 + savings_monthly) ** months)
    
    sep = "=" * 60
    
    lines = [
        f"SIMULACAO DE INVESTIMENTO - {ticker} ({stock['name']})",
        "",
        sep,
        "DADOS DO INVESTIMENTO",
        sep,
        f"  - Valor Inicial: R$ {initial_investment:,.2f}",
        f"  - Periodo: {months} meses ({months/12:.1f} anos)",
        f"  - Setor: {stock['sector']}",
        f"  - Dividend Yield Atual: {stock['dividend_yield']:.1f}% a.a.",
        "",
        sep,
        "PROJECAO (SIMULADA)",
        sep,
        f"  - Valor Final Estimado: R$ {final_value:,.2f}",
        f"  - Ganho Total: R$ {total_gain:,.2f}",
        f"  - Rentabilidade: {percentage_gain:.2f}%",
        f"  - Rentabilidade Mensal Media: {total_return_rate*100:.2f}%",
        "",
        sep,
        "COMPARATIVO (SIMULADO)",
        sep,
        f"  - {ticker}: R$ {final_value:,.2f} ({percentage_gain:+.2f}%)",
        f"  - CDI: R$ {cdi_final:,.2f} ({((cdi_final/initial_investment)-1)*100:+.2f}%)",
        f"  - Poupanca: R$ {savings_final:,.2f} ({((savings_final/initial_investment)-1)*100:+.2f}%)",
        "",
        "AVISO: Esta e uma simulacao didatica. Rentabilidade passada",
        "nao garante rentabilidade futura. Consulte um profissional.",
    ]
    return "\n".join(lines)


def get_available_tickers() -> list[str]:
    """Retorna lista de tickers disponiveis."""
    return list(MOCK_STOCK_DATA.keys())
