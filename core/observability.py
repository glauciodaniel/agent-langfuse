"""
Modulo de observabilidade com Langfuse.

Fornece integracao com Langfuse para tracking de:
- Chamadas ao LLM
- Uso de ferramentas
- Latencia e custos

Conceito Didatico - Observabilidade:
    Em producao, e essencial monitorar as chamadas ao LLM para:
    - Debuggar problemas
    - Analisar custos
    - Melhorar qualidade das respostas
    - Identificar gargalos de performance
"""

from typing import Optional, Any, Callable
from functools import lru_cache, wraps
import os

from core.config import get_settings


def _setup_langfuse_env():
    """Configura variaveis de ambiente do Langfuse."""
    settings = get_settings()
    if settings.langfuse_enabled:
        os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse_secret_key
        os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse_public_key
        os.environ["LANGFUSE_HOST"] = settings.langfuse_host


@lru_cache(maxsize=1)
def get_langfuse_client() -> Optional[Any]:
    """
    Retorna o cliente Langfuse configurado.
    
    Returns:
        Cliente Langfuse ou None se desabilitado
    """
    settings = get_settings()
    
    if not settings.langfuse_enabled:
        return None
    
    if not settings.langfuse_secret_key or not settings.langfuse_public_key:
        print("⚠️  Langfuse habilitado mas chaves nao configuradas no .env")
        return None
    
    try:
        _setup_langfuse_env()
        from langfuse import Langfuse
        
        client = Langfuse()
        print(f"✅ Langfuse conectado: {settings.langfuse_host}")
        return client
        
    except ImportError:
        print("⚠️  Langfuse nao instalado. Execute: pip install langfuse")
        return None
    except Exception as e:
        print(f"⚠️  Erro ao conectar Langfuse: {e}")
        return None


def langfuse_observe(name: str = None):
    """
    Decorator para observar funcoes com Langfuse.
    
    Usa o decorator @observe do Langfuse se habilitado,
    caso contrario apenas executa a funcao normalmente.
    
    Args:
        name: Nome do span (opcional)
    """
    def decorator(func: Callable) -> Callable:
        settings = get_settings()
        
        if not settings.langfuse_enabled:
            return func
        
        try:
            _setup_langfuse_env()
            from langfuse import observe
            
            # Aplicar o decorator observe do Langfuse
            decorated = observe(name=name or func.__name__)(func)
            return decorated
            
        except ImportError:
            return func
        except Exception:
            return func
    
    return decorator


def flush_langfuse() -> None:
    """
    Forca o envio de dados pendentes para o Langfuse.
    """
    client = get_langfuse_client()
    if client:
        try:
            client.flush()
        except Exception:
            pass


def update_trace_context(session_id: str = None, user_id: str = None, metadata: dict = None):
    """
    Atualiza o trace atual com informacoes de contexto.
    
    Deve ser chamado dentro de uma funcao decorada com @observe.
    
    Args:
        session_id: ID da sessao para agrupar traces
        user_id: ID do usuario
        metadata: Metadados extras
    """
    settings = get_settings()
    if not settings.langfuse_enabled:
        return
    
    try:
        _setup_langfuse_env()
        from langfuse import Langfuse
        
        client = Langfuse()
        client.update_current_trace(
            session_id=session_id,
            user_id=user_id,
            metadata=metadata
        )
    except Exception as e:
        # Silenciosamente ignora erros de contexto
        pass
