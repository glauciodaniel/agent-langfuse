"""
Ferramentas (Tools) do Agente LangChain.

Conceito Didatico - Tools em LangChain:
    Tools sao funcoes que o LLM pode "chamar" quando precisa
    de informacoes externas. O uso de Pydantic garante que
    o LLM envie os parametros corretos.

Este arquivo contem APENAS as definicoes de tools,
separando a logica de negocio (market_data) das tools.
"""

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from domain.market_data import (
    get_stock_price,
    compare_stocks,
    get_market_summary,
    calculate_investment_returns,
    get_available_tickers,
)


# =============================================================================
# SCHEMAS DE ENTRADA (Pydantic)
# =============================================================================

class StockPriceInput(BaseModel):
    """Schema para consulta de preco."""
    ticker: str = Field(
        description="Codigo da acao brasileira (ex: PETR4, VALE3, ITUB4)"
    )


class CompareStocksInput(BaseModel):
    """Schema para comparacao de acoes."""
    ticker1: str = Field(description="Codigo da primeira acao (ex: PETR4)")
    ticker2: str = Field(description="Codigo da segunda acao (ex: VALE3)")


class CalculateReturnsInput(BaseModel):
    """Schema para calculo de rendimentos."""
    ticker: str = Field(description="Codigo da acao (ex: PETR4)")
    initial_investment: float = Field(
        description="Valor inicial em reais (ex: 10000.00)",
        gt=0
    )
    months: int = Field(
        description="Periodo em meses (ex: 12)",
        gt=0,
        le=120
    )


# =============================================================================
# DEFINICAO DAS TOOLS
# =============================================================================

@tool(args_schema=StockPriceInput)
def stock_price_tool(ticker: str) -> str:
    """
    Busca o preco atual de uma acao brasileira.
    
    Use quando o usuario perguntar:
    - Preco de uma acao especifica
    - Cotacao de empresas
    - "Quanto esta", "Qual o valor"
    
    Exemplos:
    - "Quanto esta a Petrobras?" -> ticker='PETR4'
    - "Preco da Vale?" -> ticker='VALE3'
    """
    return get_stock_price(ticker)


@tool(args_schema=CompareStocksInput)
def compare_stocks_tool(ticker1: str, ticker2: str) -> str:
    """
    Compara duas acoes brasileiras lado a lado.
    
    Use quando o usuario quiser:
    - Comparar duas acoes
    - Decidir entre opcoes de investimento
    - Ver qual acao esta melhor
    
    Exemplos:
    - "Compare Petrobras e Vale" -> ticker1='PETR4', ticker2='VALE3'
    - "Itau ou Bradesco?" -> ticker1='ITUB4', ticker2='BBDC4'
    """
    return compare_stocks(ticker1, ticker2)


@tool
def market_summary_tool() -> str:
    """
    Retorna resumo completo do mercado financeiro brasileiro.
    
    Use quando o usuario perguntar:
    - Visao geral do mercado
    - Como esta o Ibovespa
    - Quais acoes estao em alta ou baixa
    - Resumo do dia
    
    Nao precisa de parametros.
    """
    return get_market_summary()


@tool(args_schema=CalculateReturnsInput)
def calculate_returns_tool(ticker: str, initial_investment: float, months: int) -> str:
    """
    Simula rendimentos de um investimento em uma acao.
    
    Use quando o usuario quiser:
    - Simular um investimento
    - Calcular quanto teria se investisse
    - Comparar rendimento com CDI ou poupanca
    - Projetar ganhos futuros
    
    Exemplos:
    - "Se investir 10 mil em Petrobras por 1 ano" -> ticker='PETR4', initial_investment=10000, months=12
    """
    return calculate_investment_returns(ticker, initial_investment, months)


@tool
def list_available_stocks_tool() -> str:
    """
    Lista todas as acoes disponiveis para consulta.
    
    Use quando o usuario perguntar:
    - Quais acoes estao disponiveis
    - Que empresas posso consultar
    - Lista de tickers
    """
    tickers = get_available_tickers()
    return f"Acoes disponiveis: {', '.join(tickers)}"


# Lista de todas as ferramentas (facilita importacao)
ALL_TOOLS = [
    stock_price_tool,
    compare_stocks_tool,
    market_summary_tool,
    calculate_returns_tool,
    list_available_stocks_tool,
]
