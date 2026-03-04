"""
Tipos e estruturas de dados do agente.

Conceito Didatico - Dataclasses vs Dicionarios:
    Usar dataclasses ao inves de dicts traz:
    - Autocomplete no IDE
    - Validacao de tipos
    - Documentacao embutida
    - Codigo mais legivel
"""

from dataclasses import dataclass, field
from typing import Any, Literal
from datetime import datetime


LogType = Literal["action", "observation", "answer", "error", "thought"]


@dataclass
class ExecutionLog:
    """
    Representa um log de execucao do agente.
    
    Attributes:
        type: Tipo do log (action, observation, answer, error)
        content: Conteudo principal do log
        tool: Nome da ferramenta (se type == action)
        args: Argumentos da ferramenta (se type == action)
        timestamp: Momento da execucao
    """
    type: LogType
    content: str = ""
    tool: str | None = None
    args: dict[str, Any] | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Converte para dicionario (compatibilidade)."""
        result = {"type": self.type}
        if self.content:
            result["content"] = self.content
        if self.tool:
            result["tool"] = self.tool
        if self.args:
            result["args"] = self.args
        return result


@dataclass
class AgentResponse:
    """
    Resposta completa do agente.
    
    Attributes:
        answer: Resposta textual final
        logs: Lista de logs de execucao
        success: Se a execucao foi bem sucedida
        error: Mensagem de erro (se houver)
    """
    answer: str
    logs: list[ExecutionLog] = field(default_factory=list)
    success: bool = True
    error: str | None = None
    
    @property
    def used_tools(self) -> list[str]:
        """Retorna lista de ferramentas usadas."""
        return [log.tool for log in self.logs if log.type == "action" and log.tool]
