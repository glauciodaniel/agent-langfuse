"""
Logica principal do agente ReAct.

Este modulo contem APENAS a logica do loop ReAct, mantendo
o codigo limpo e focado em uma unica responsabilidade.

Conceito Didatico - Single Responsibility:
    Cada modulo deve ter uma unica razao para mudar.
    Este modulo so muda se a logica do agente mudar,
    nao se mudarmos prompts, ferramentas ou configuracoes.
"""

from typing import Optional
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
import openai
import httpx

from core.config import get_settings
from core.memory import ConversationMemory
from common.types import ExecutionLog, AgentResponse
from common.exceptions import (
    AgentError,
    RateLimitError,
    NetworkError,
    AuthenticationError,
    ToolExecutionError,
)
from domain.tools import ALL_TOOLS


def load_system_prompt() -> str:
    """
    Carrega o prompt do sistema de arquivo externo.
    
    Conceito Didatico - Prompts Externalizados:
        Manter prompts em arquivos separados permite:
        - Versionar prompts independentemente do codigo
        - Editar prompts sem tocar no codigo
        - Ter diferentes prompts para diferentes ambientes
        - Facilitar testes A/B de prompts
    
    Returns:
        Conteudo do prompt do sistema
    """
    prompt_path = Path(__file__).parent.parent / "prompts" / "system_prompt.txt"
    
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    
    # Fallback para prompt embutido (caso arquivo nao exista)
    return """Voce e um Analista Financeiro Junior prestativo e preciso.
Responda perguntas sobre o mercado financeiro brasileiro.
Use as ferramentas disponiveis quando necessario.
Sempre responda em portugues brasileiro."""


def create_llm() -> ChatOpenAI:
    """
    Cria instancia do modelo LLM com ferramentas.
    
    Returns:
        Modelo configurado com tools
    """
    settings = get_settings()
    
    llm = ChatOpenAI(
        model=settings.model,
        temperature=settings.temperature,
        max_retries=settings.max_retries,
        timeout=settings.timeout,
    )
    
    return llm.bind_tools(ALL_TOOLS)


def handle_api_error(error: Exception) -> AgentError:
    """
    Converte excecoes de API em excecoes do agente.
    
    Args:
        error: Excecao original
        
    Returns:
        Excecao do agente apropriada
    """
    error_str = str(error).lower()
    
    # Rate limit
    if "rate limit" in error_str or isinstance(error, openai.RateLimitError):
        return RateLimitError(str(error))
    
    # Autenticacao
    if "authentication" in error_str or isinstance(error, openai.AuthenticationError):
        return AuthenticationError(str(error))
    
    # Rede
    if isinstance(error, (httpx.ConnectError, httpx.TimeoutException, ConnectionError)):
        return NetworkError(str(error))
    
    # Generico
    return AgentError(str(error), f"Erro inesperado: {str(error)}")


def run_agent(
    query: str,
    memory: Optional[ConversationMemory] = None,
) -> AgentResponse:
    """
    Executa o agente com uma pergunta do usuario.
    
    Implementa o loop ReAct:
    1. Recebe pergunta do usuario
    2. Envia ao LLM com historico
    3. Se LLM pedir tool: executa e volta ao passo 2
    4. Se LLM responder: retorna resposta final
    
    Args:
        query: Pergunta do usuario
        memory: Memoria de conversacao (opcional)
        
    Returns:
        AgentResponse com resposta e logs de execucao
    """
    settings = get_settings()
    
    # Criar memoria se nao fornecida
    if memory is None:
        memory = ConversationMemory(max_messages=settings.memory_max_messages)
    
    # Adicionar pergunta a memoria
    memory.add_user_message(query)
    
    logs: list[ExecutionLog] = []
    
    try:
        # Criar modelo
        llm = create_llm()
        
        # Criar mapa de ferramentas
        tools_map = {tool.name: tool for tool in ALL_TOOLS}
        
        # Montar mensagens: system + historico
        system_prompt = load_system_prompt()
        messages = [("system", system_prompt)]
        messages.extend(memory.get_messages())
        
        # Loop ReAct
        for iteration in range(settings.max_iterations):
            # Invocar modelo
            response = llm.invoke(messages)
            
            # Se nao ha tool calls, temos a resposta final
            if not response.tool_calls:
                logs.append(ExecutionLog(type="answer", content=response.content))
                memory.add_assistant_message(response.content)
                
                return AgentResponse(
                    answer=response.content,
                    logs=logs,
                    success=True,
                )
            
            # Processar tool calls
            messages.append(response)
            
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]
                
                # Log da acao
                logs.append(ExecutionLog(
                    type="action",
                    tool=tool_name,
                    args=tool_args,
                ))
                
                # Executar ferramenta
                if tool_name not in tools_map:
                    tool_result = f"Erro: Ferramenta '{tool_name}' nao encontrada."
                else:
                    try:
                        tool_result = tools_map[tool_name].invoke(tool_args)
                    except Exception as e:
                        tool_result = f"Erro ao executar: {str(e)}"
                
                # Log da observacao
                logs.append(ExecutionLog(type="observation", content=tool_result))
                
                # Adicionar resultado ao historico
                messages.append(ToolMessage(content=tool_result, tool_call_id=tool_id))
        
        # Excedeu iteracoes
        error_msg = "Nao consegui processar a solicitacao no tempo limite."
        memory.add_assistant_message(error_msg)
        
        return AgentResponse(
            answer=error_msg,
            logs=logs,
            success=False,
            error="Max iterations exceeded",
        )
        
    except openai.APIError as e:
        agent_error = handle_api_error(e)
        logs.append(ExecutionLog(type="error", content=str(e)))
        
        return AgentResponse(
            answer=agent_error.user_message,
            logs=logs,
            success=False,
            error=str(e),
        )
        
    except Exception as e:
        agent_error = handle_api_error(e)
        logs.append(ExecutionLog(type="error", content=str(e)))
        
        return AgentResponse(
            answer=agent_error.user_message,
            logs=logs,
            success=False,
            error=str(e),
        )


def run_agent_simple(
    query: str,
    memory: Optional[ConversationMemory] = None,
) -> str:
    """
    Versao simplificada que retorna apenas a resposta.
    
    Args:
        query: Pergunta do usuario
        memory: Memoria de conversacao (opcional)
        
    Returns:
        Resposta textual do agente
    """
    response = run_agent(query, memory)
    return response.answer
