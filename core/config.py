"""
Configuracoes centralizadas do agente.

Conceito Didatico - Configuracao Centralizada:
    Ter todas as configuracoes em um unico lugar permite:
    - Facil manutencao e alteracao
    - Validacao de valores
    - Documentacao clara do que e configuravel
    - Evitar duplicacao de codigo
"""

import os
from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv

# Carregar .env no inicio
load_dotenv(override=True)


@dataclass(frozen=True)
class Settings:
    """
    Configuracoes do agente.
    
    Conceito Didatico - Dataclass Frozen:
        frozen=True torna a classe imutavel, garantindo que
        as configuracoes nao sejam alteradas acidentalmente
        durante a execucao.
    
    Attributes:
        openai_api_key: Chave de API da OpenAI
        model: Nome do modelo LLM
        temperature: Criatividade do modelo (0-1)
        max_retries: Tentativas em caso de erro
        timeout: Timeout em segundos
        max_iterations: Maximo de iteracoes do loop ReAct
        memory_max_messages: Maximo de mensagens na memoria
    """
    # API
    openai_api_key: str
    model: str = "gpt-4"
    temperature: float = 0.0
    max_retries: int = 3
    timeout: float = 30.0

    # Agent
    max_iterations: int = 5
    memory_max_messages: int = 20
    
    @classmethod
    def from_env(cls) -> "Settings":
        """
        Cria Settings a partir de variaveis de ambiente.
        
        Returns:
            Instancia de Settings com valores do ambiente
            
        Raises:
            ValueError: Se OPENAI_API_KEY nao estiver configurada
        """
        api_key = os.getenv("OPENAI_API_KEY", "")
        
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY nao configurada. "
                "Edite o arquivo .env e adicione sua chave."
            )
        
        return cls(
            openai_api_key=api_key,
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0")),
            max_retries=int(os.getenv("OPENAI_MAX_RETRIES", "3")),
            timeout=float(os.getenv("OPENAI_TIMEOUT", "30")),
            max_iterations=int(os.getenv("AGENT_MAX_ITERATIONS", "5")),
            memory_max_messages=int(os.getenv("AGENT_MEMORY_MAX_MESSAGES", "20")),
        )
    
    def to_dict(self) -> dict:
        """Retorna configuracoes como dicionario (sem API key)."""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "max_iterations": self.max_iterations,
            "memory_max_messages": self.memory_max_messages,
        }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Retorna instancia singleton das configuracoes.
    
    Conceito Didatico - lru_cache:
        O decorator @lru_cache garante que a funcao so
        executa uma vez, retornando o mesmo objeto em
        chamadas subsequentes. Isso e util para:
        - Evitar leitura repetida de .env
        - Garantir consistencia de configuracoes
        - Performance (carregar uma vez)
    
    Returns:
        Instancia de Settings
    """
    return Settings.from_env()


def validate_api_key() -> bool:
    """
    Verifica se a API key esta configurada.
    
    Returns:
        True se a chave existe e parece valida
    """
    key = os.getenv("OPENAI_API_KEY", "")
    return bool(key) and key != "sua-chave-aqui"
