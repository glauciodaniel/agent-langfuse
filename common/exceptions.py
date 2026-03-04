"""
Excecoes customizadas do agente.

Conceito Didatico - Hierarquia de Excecoes:
    Criar excecoes especificas permite:
    - Tratamento granular de erros
    - Mensagens mais claras para o usuario
    - Facilidade de debug e logging
    - Codigo mais expressivo
"""


class AgentError(Exception):
    """Excecao base para erros do agente."""
    
    def __init__(self, message: str, user_message: str | None = None):
        """
        Args:
            message: Mensagem tecnica (para logs)
            user_message: Mensagem amigavel (para exibir ao usuario)
        """
        super().__init__(message)
        self.user_message = user_message or message


class APIError(AgentError):
    """Excecao para erros de comunicacao com API."""
    pass


class RateLimitError(APIError):
    """Excecao para quando atingimos o limite de requisicoes."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            user_message=(
                "Desculpe, estamos recebendo muitas requisicoes no momento. "
                "Por favor, aguarde alguns segundos e tente novamente."
            )
        )


class NetworkError(APIError):
    """Excecao para erros de rede."""
    
    def __init__(self, message: str = "Network error"):
        super().__init__(
            message=message,
            user_message=(
                "Erro de conexao com a API. "
                "Verifique sua conexao com a internet e tente novamente."
            )
        )


class AuthenticationError(APIError):
    """Excecao para erros de autenticacao."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            user_message=(
                "Erro de autenticacao com a API. "
                "Verifique se sua OPENAI_API_KEY esta configurada corretamente."
            )
        )


class ToolExecutionError(AgentError):
    """Excecao para erros na execucao de ferramentas."""
    
    def __init__(self, tool_name: str, message: str):
        super().__init__(
            message=f"Erro ao executar '{tool_name}': {message}",
            user_message=f"Houve um problema ao consultar os dados. Tente novamente."
        )
        self.tool_name = tool_name
