"""
Gerenciamento de memoria do agente.

Conceito Didatico - Memoria em Agentes:
    Existem varios tipos de memoria em agentes de IA:
    
    1. Buffer Memory (usado aqui):
       - Guarda todas as mensagens ate um limite
       - Simples e eficaz para conversas curtas
       
    2. Summary Memory:
       - Resume conversas longas periodicamente
       - Economiza tokens mas perde detalhes
       
    3. Window Memory:
       - Guarda apenas as ultimas N mensagens
       - Facil de implementar, perde contexto antigo
       
    4. Vector Memory:
       - Armazena em banco vetorial
       - Busca por similaridade semantica
       - Ideal para bases de conhecimento grandes
"""

from typing import List, Optional
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage


class ConversationMemory:
    """
    Gerenciador de memoria de conversacao usando Buffer Memory.
    
    Attributes:
        messages: Lista de mensagens da conversa
        max_messages: Limite de mensagens a manter
    """
    
    def __init__(self, max_messages: int = 20):
        """
        Inicializa a memoria.
        
        Args:
            max_messages: Numero maximo de mensagens a manter
        """
        self._messages: List[BaseMessage] = []
        self._max_messages = max_messages
    
    @property
    def messages(self) -> List[BaseMessage]:
        """Retorna copia da lista de mensagens."""
        return self._messages.copy()
    
    @property
    def max_messages(self) -> int:
        """Retorna limite de mensagens."""
        return self._max_messages
    
    def add_user_message(self, content: str) -> None:
        """
        Adiciona mensagem do usuario.
        
        Args:
            content: Texto da mensagem
        """
        self._messages.append(HumanMessage(content=content))
        self._trim_if_needed()
    
    def add_assistant_message(self, content: str) -> None:
        """
        Adiciona resposta do assistente.
        
        Args:
            content: Texto da resposta
        """
        self._messages.append(AIMessage(content=content))
        self._trim_if_needed()
    
    def add_message(self, message: BaseMessage) -> None:
        """
        Adiciona uma mensagem generica.
        
        Args:
            message: Objeto de mensagem LangChain
        """
        self._messages.append(message)
        self._trim_if_needed()
    
    def get_messages(self) -> List[BaseMessage]:
        """Retorna copia do historico de mensagens."""
        return self._messages.copy()
    
    def clear(self) -> None:
        """Limpa toda a memoria."""
        self._messages = []
    
    def _trim_if_needed(self) -> None:
        """Remove mensagens antigas se exceder o limite."""
        if len(self._messages) > self._max_messages:
            self._messages = self._messages[-self._max_messages:]
    
    def __len__(self) -> int:
        """Retorna numero de mensagens."""
        return len(self._messages)
    
    def __repr__(self) -> str:
        """Representacao para debug."""
        return f"ConversationMemory({len(self._messages)} mensagens)"
    
    def get_summary(self) -> str:
        """Retorna resumo da memoria para exibicao."""
        return f"Memoria: {len(self._messages)} mensagens armazenadas"


# Singleton global para memoria persistente na sessao
_global_memory: Optional[ConversationMemory] = None


def get_global_memory() -> ConversationMemory:
    """
    Retorna a instancia global de memoria.
    
    Conceito Didatico - Singleton Pattern:
        O padrao Singleton garante que existe apenas
        uma instancia da memoria durante toda a sessao.
        Isso permite persistencia entre chamadas.
    
    Returns:
        Instancia global de ConversationMemory
    """
    global _global_memory
    if _global_memory is None:
        _global_memory = ConversationMemory()
    return _global_memory


def clear_global_memory() -> None:
    """Limpa a memoria global."""
    global _global_memory
    if _global_memory is not None:
        _global_memory.clear()
